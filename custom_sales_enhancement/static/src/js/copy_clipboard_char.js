/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";
import { useService } from "@web/core/utils/hooks";

/**
 * Clipboard Widget for Char Fields - v18 Compatible
 * Requirement 10: Add New widget for char field to copy the content into clipboard
 */
export class ClipboardCharField extends CharField {
    static template = "custom_sales_enhancement.ClipboardCharField";

    setup() {
        super.setup();
        this.notification = useService("notification");
    }

    async copyToClipboard() {
        const value = this.props.record.data[this.props.name] || '';

        if (!value) {
            this.notification.add("No content to copy", { type: 'warning' });
            return;
        }

        try {
            if (navigator.clipboard && window.isSecureContext) {
                // Use the modern Clipboard API
                await navigator.clipboard.writeText(value);
            } else {
                // Fallback for older browsers or non-secure contexts
                const textArea = document.createElement('textarea');
                textArea.value = value;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                textArea.style.top = '-999999px';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();

                const successful = document.execCommand('copy');
                document.body.removeChild(textArea);

                if (!successful) {
                    throw new Error('Fallback copy method failed');
                }
            }

            // Show success notification
            this.notification.add(`Copied "${value}" to clipboard!`, {
                type: 'success',
                sticky: false
            });

        } catch (err) {
            console.error('Failed to copy to clipboard:', err);
            this.notification.add('Failed to copy to clipboard', {
                type: 'danger',
                sticky: false
            });
        }
    }

    get isReadonly() {
        return this.props.readonly;
    }

    get hasValue() {
        return Boolean(this.props.record.data[this.props.name]);
    }
}

// Register the widget
registry.category("fields").add("clipboard_char", ClipboardCharField);