import bind from 'lodash/bind';
import each from 'lodash/each';
import reject from 'lodash/reject';


/**
 * This function returns a stateful mixin.
 */
L.singleClickEventMixin = function(){
    /*
     * Since this mixin object is stateful, it is important for a new mixin object to
     * be returned every time. Otherwise, objects that use the mixin could inadvertently share state.
     */

    return {

        dblclickInterval : 500,

        _hasAddedClickHandler : false,

        _addClickEventHandlers : function() {
            var self = this;

            var timeout;

            var clearClickTimeout = function() {
                if (timeout) {
                    window.clearTimeout(timeout);
                    timeout = undefined;
                }
            };

            var checkLater = function(ev) {
                if (this._singleClickHandlers.length > 0) {
                    window.clearTimeout(timeout);
                    timeout = window.setTimeout(function() {
                        each(self._singleClickHandlers, function(handler) {
                            handler.boundHandler(ev);
                        });
                    }, this.dblclickInterval);
                }
            };

            if (this.on) {
                this.on('click', checkLater);
                this.on('dblclick', clearClickTimeout);
            }
        },

        addSingleClickHandler : function(handler, context) {
            if (!this._hasAddedClickHandler) {
                this._addClickEventHandlers();
                this._hasAddedClickHandler = true;
            }

            this._singleClickHandlers.push({
                handler : handler,
                boundHandler : bind(handler, context)
            });
        },

        removeSingleClickHandler : function(handler) {
            this._singleClickHandlers = reject(this._singleClickHandlers, function(thisHandler) {
                return thisHandler.handler === handler;
            });
        },

        _singleClickHandlers : []

    };
};
