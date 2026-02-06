# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
from contextlib import suppress
from enum import Enum

from werkzeug.exceptions import NotFound
from werkzeug.routing import Map, Submount
from werkzeug.wrappers import Request, Response

import frappe
from frappe import _
from frappe.modules.utils import get_doctype_app_map
from frappe.monitor import add_data_to_monitor
from frappe.utils.response import build_response
from frappe.utils.telemetry.pulse.app_heartbeat_event import capture_app_heartbeat

# --- Custom Imports Start ---
from bs4 import BeautifulSoup
from frappe.core.api.file import get_max_file_size
from frappe.translate import get_all_translations
from frappe.utils import cstr, split_emails, validate_email_address
from frappe.utils.telemetry import POSTHOG_HOST_FIELD, POSTHOG_PROJECT_FIELD
from semantic_version import Version
# --- Custom Imports End ---

class ApiVersion(str, Enum):
        V1 = "v1"
        V2 = "v2"


def handle(request: Request):
        """
        Entry point for `/api` methods.

        APIs are versioned using second part of path.
        v1 -> `/api/v1/*`
        v2 -> `/api/v2/*`

        Different versions have different specification but broadly following things are supported:

        - `/api/method/{methodname}` will call a whitelisted method
        - `/api/resource/{doctype}` will query a table
                examples:
                - `?fields=["name", "owner"]`
                - `?filters=[["Task", "name", "like", "%005"]]`
                - `?limit_start=0`
                - `?limit_page_length=20`
        - `/api/resource/{doctype}/{name}` will point to a resource
                `GET` will return document
                `POST` will insert
                `PUT` will update
                `DELETE` will delete
        """

        try:
                endpoint, arguments = API_URL_MAP.bind_to_environ(request.environ).match()
        except NotFound:  # Wrap 404 - backward compatiblity
                raise frappe.DoesNotExistError

        data = endpoint(**arguments)
        if isinstance(data, Response):
                return data

        if data is not None:
                frappe.response["data"] = data
        data = build_response("json")

        with suppress(Exception):
                method = arguments.get("method") or frappe.form_dict.get("method")
                doctype = arguments.get("doctype") or frappe.form_dict.get("doctype")
                if method or doctype:
                        app_name = None
                        if doctype:
                                app_name = get_doctype_app_map().get(doctype)
                        elif method and "." in method:
                                app_name = method.split(".", 1)[0]
                        if app_name:
                                add_data_to_monitor(app=app_name)
                                capture_app_heartbeat(app_name)

        return data


# Merge all API version routing rules
from frappe.api.v1 import url_rules as v1_rules
from frappe.api.v2 import url_rules as v2_rules

API_URL_MAP = Map(
        [
                # V1 routes
                Submount("/api", v1_rules),
                Submount(f"/api/{ApiVersion.V1.value}", v1_rules),
                Submount(f"/api/{ApiVersion.V2.value}", v2_rules),
        ],
        strict_slashes=False,  # Allows skipping trailing slashes
        merge_slashes=False,
)


def get_api_version() -> ApiVersion | None:
        if not frappe.request:
                return

        if frappe.request.path.startswith(f"/api/{ApiVersion.V2.value}"):
                return ApiVersion.V2
        return ApiVersion.V1

# --- Custom Functions Start ---

def is_frappe_version(version, above=False):
	frappe_version = Version(frappe.__version__)
	target_version = Version(version)
	
	if above:
		return frappe_version >= target_version
	return frappe_version.major == target_version.major


@frappe.whitelist(allow_guest=True)
def get_translations():
	if frappe.session.user != "Guest":
		language = frappe.db.get_value("User", frappe.session.user, "language")
	else:
		language = frappe.db.get_single_value("System Settings", "language")

	return get_all_translations(language)


@frappe.whitelist()
def get_user_signature():
	user = frappe.session.user
	user_email_signature = (
		frappe.db.get_value(
			"User",
			user,
			"email_signature",
		)
		if user
		else None
	)

	signature = user_email_signature or frappe.db.get_value(
		"Email Account",
		{"default_outgoing": 1, "add_signature": 1},
		"signature",
	)

	if not signature:
		return

	soup = BeautifulSoup(signature, "html.parser")
	html_signature = soup.find("div", {"class": "ql-editor read-mode"})
	_signature = None
	if html_signature:
		_signature = html_signature.renderContents()
	content = ""
	if cstr(_signature) or signature:
		content = f'<br><p class="signature">{signature}</p>'
	return content


@frappe.whitelist()
def get_posthog_settings():
	return {
		"posthog_project_id": frappe.conf.get(POSTHOG_PROJECT_FIELD),
		"posthog_host": frappe.conf.get(POSTHOG_HOST_FIELD),
		"enable_telemetry": frappe.get_system_settings("enable_telemetry"),
		"telemetry_site_age": frappe.utils.telemetry.site_age(),
	}


def check_app_permission():
	if frappe.session.user == "Administrator":
		return True

	allowed_modules = []

	if is_frappe_version("15"):
		allowed_modules = frappe.config.get_modules_from_all_apps_for_user()
	elif is_frappe_version("16", above=True):
		allowed_modules = frappe.utils.modules.get_modules_from_all_apps_for_user()

	allowed_modules = [x["module_name"] for x in allowed_modules]
	if "FCRM" not in allowed_modules:
		return False

	roles = frappe.get_roles()
	if any(role in ["System Manager", "Sales User", "Sales Manager"] for role in roles):
		return True

	return False


@frappe.whitelist(allow_guest=True)
def accept_invitation(key: str | None = None):
	if not key:
		frappe.throw(_("Invalid or expired key"))

	result = frappe.db.get_all("CRM Invitation", filters={"key": key}, pluck="name")
	if not result:
		frappe.throw(_("Invalid or expired key"))
	invitation = frappe.get_doc("CRM Invitation", result[0])
	invitation.accept()
	invitation.reload()

	if invitation.status == "Accepted":
		frappe.local.login_manager.login_as(invitation.email)
# --- Custom Functions End ---
