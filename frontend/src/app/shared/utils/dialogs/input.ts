import { Popup } from '@utils'
import * as $ from 'jquery';

let ALREADY_OPEN = false;

export class Input_ extends Popup {

        constructor(msg = '', options = {}, callback = null) {
            super(msg, options, callback);
        }

        open() {
            let class_ = '';

            switch (this.options.size) {
                case 's' || 'S': class_ = 'popup-sm'
                    break;
                case 'm' || 'M': class_ = 'popup-md'
                    break;
                case 'l' || 'L': class_ = 'popup-lg'
                    break;
            }

            if (!ALREADY_OPEN) {
                const div = $('<div>', { id: 'popup_div_inner', name: 'popupInner', class: 'popup fadeIn2 ' + class_ });
                const div2 = $('<div>', { id: 'backdrop_popup', name: 'popupBackdrop', class: 'fadeIn1 backdrop_popup' });
                const card = $('<div>', { id: 'card_popup', name: 'card_popup', class: 'card', style: 'z-index: 1400;' });
                const header = $('<div>', { id: 'card_header', name: 'card_header', class: 'card-header',
                                            html: '<span>' + this.options.header + '</span>',
                                            style: 'background-color: ' + this.options.backgroundColor +
                                                   '; color: ' + this.options.textColor + ';' });
                const body = $('<div>', { id: 'card_body', name: 'card_body', class: 'card-block',
                                         html: '<div class="col-sm-12"><span>' + this.msg + '</span><input style="width: 100%" type="' +
                                               this.options.input_type + '"class="input input-sm" id="input_popup" /></div>' });
                const footer = $('<div>', { id: 'card_footer', name: 'card_footer', class: 'card-footer',
                                            style: 'background-color: ' + this.options.backgroundColor +
                                                    '; color: ' + this.options.textColor + ';' });
                this.options.buttons.forEach((button => {
                    const button_ = $('<button>', { id: 'button' + button['name'], type: 'button', name: 'button' + button['name'],
                                                    class: button['class'], html: button['name'] });
                    button_.click(() => {
                        if (this.callback) {
                            this.callback(button['return'], $('#input_popup').val());
                        }
                        if (button['close']) {
                            this.close();
                        }
                    });
                    footer.append(button_);
                }));
                card.append(header);
                card.append(body);
                card.append(footer);
                div.append(div2);
                div.append(card);
                $('#popup_div').append(div);
                $('#input_popup').focus();
                ALREADY_OPEN = true;
            }
        }

        close() {
            super.close();
            ALREADY_OPEN = false;
        }
    }

    export default Input_;
