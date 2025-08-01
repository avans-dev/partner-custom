/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

// Import the existing Odoo copy clipboard components
import { CopyClipboardCharField } from "@web/views/fields/copy_clipboard/copy_clipboard_field";

// Import TextField for text field support
import { TextField } from "@web/views/fields/text/text_field";
import { CopyButton } from "@web/core/copy_button/copy_button";
import { evaluateBooleanExpr } from "@web/core/py_js/py";
import { omit } from "@web/core/utils/objects";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component } from "@odoo/owl";

// Function to extract props (reuse from original)
function extractProps({ attrs }) {
    return {
        string: attrs.string,
        disabledExpr: attrs.disabled,
    };
}

// Register custom widgets with different names using existing components

export const CopyCharField = {
    component: CopyClipboardCharField,
    supportedTypes: ["char"],
    extractProps,
};

// Register the custom widgets
registry.category("fields").add("copy_char", CopyCharField);
