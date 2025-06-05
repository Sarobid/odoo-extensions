const eventChanelService = {
    sav_mec_piece_refresh : function (session,channel,message) {
        // console.log('eventChanelService.sav_mec_piece_refresh', session, channel, message, window.is_mecano);
        if (session.uid && window.is_mecano) {
            if (channel === 'sav_mec_piece_refresh') {
                // console.log('sav_mec_piece_refresh', message);
                if (message['message']) {
                    paramUrl = "web#action=" + message['message'];
                    // console.log('sav_mec_piece_refresh', paramUrl);
                    if(window.location.href.indexOf(paramUrl) === -1) {
                        window.location.href = paramUrl;
                    }else {
                        // console.log('sav_mec_piece_refresh', message);
                        window.location.reload();
                    }   
                }
            }   
        }
    }
}