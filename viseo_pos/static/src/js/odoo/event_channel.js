odoo.define('viseo_pos.event.channel', function (require) {
    "use strict";

    const LongpollingBus = require('bus.Longpolling');
    const session = require('web.session');
    

    const CustomLongpolling = LongpollingBus.include({
    
        startPolling: function () {
            this.addChannel('sav_mec_piece_refresh');
            this._super.apply(this, arguments);
        },
        _onPoll: function (notifications) {
            const notifs = this._super.apply(this, arguments);

            notifs.forEach(([channel, message]) => {
                // if (channel === 'sav_mec_piece_refresh') {
                //     console.log('sav_mec_piece_refresh', message);
                //     window.location.href = "web#action="+message;
                //     // Tu peux ici déclencher une action custom : reload, toast, etc.
                // } else {
                //     console.log('[🛠 Autre notification]', { channel, message });
                // }
                // eventChanelService.sav_mec_piece_refresh(session,channel, message);
            });

            return notifs;
        },
    });

    return CustomLongpolling;
});





