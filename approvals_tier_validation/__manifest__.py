# Copyright 2017-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Approvals Tier Validation",
    "version": "13.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/server-ux",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["base_tier_validation"],
    "data": [
        "security/ir.model.access.csv",
        "security/tier_approval_security.xml",
        "views/tier_approval_category_views.xml",
        "views/tier_approval_views.xml",
    ],
    "development_status": "alpha",
    "maintainers": ["kittiu"],
    "application": False,
    "installable": True,
}
