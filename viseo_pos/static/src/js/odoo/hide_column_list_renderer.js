odoo.define('viseo_pos.hide_column_list_renderer', function (require) {
    "use strict";

    const ListRenderer = require('web.ListRenderer');

    const HideColumnListRenderer = ListRenderer.include({

        _renderBodyCell(record, node, colIndex, options) {
            const $cell = this._super.apply(this, arguments);

            if (node.attrs.name === 'state_sav_mec_display' && record.data.is_sav_mec === false) {
                $cell.addClass('o_hidden_column');
            }

            return $cell;
        },

        _renderHeader(isGrouped) {
            const $thead = this._super.apply(this, arguments);

            const anyVisible = this.state.data.some(record => record.data.is_sav_mec);
            if (!anyVisible) {
                $thead.find('th[data-name="state_sav_mec_display"]').addClass('o_hidden_column');
            }

            return $thead;
        },
    });

    return HideColumnListRenderer;
});
