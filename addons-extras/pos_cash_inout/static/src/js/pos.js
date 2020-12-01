openerp.pos_cash_inout = function(instance) {
	var module = instance.point_of_sale;
	var _t = instance.web._t;
	var QWeb = instance.web.qweb;

	var round_di = instance.web.round_decimals;
	var round_pr = instance.web.round_precision;

	var models = module.PosModel.prototype.models;
	for (var i = 0; i < models.length; i++) {
		var model = models[i];
		if (model.model === 'cash.box.in') {
			model.fields.push('name');
			model.fields.push('amount');
		} 
	}

	module.PosWidget.include({
		build_widgets : function() {
			var self = this;
			this._super();
			pos = this.pos;
			move = false;
			var msg_show_take_money_out = "";
			var msg_show_put_money_in = "";

			this.custom_dialog_box_take_money_out = new module.custom_dialog_box_take_money_out(this, {});
			this.custom_dialog_box_take_money_out.appendTo(this.$el);
			this.screen_selector.popup_set['custom_dialog_box_take_money_out'] = this.custom_dialog_box_take_money_out;
			this.custom_dialog_box_take_money_out.hide();

			this.custom_dialog_box_put_money_in = new module.custom_dialog_box_put_money_in(this, {});
			this.custom_dialog_box_put_money_in.appendTo(this.$el);
			this.screen_selector.popup_set['custom_dialog_box_put_money_in'] = this.custom_dialog_box_put_money_in;
			this.custom_dialog_box_put_money_in.hide();

			var put_money_in = $(QWeb.render('PutMoneyIn'));
			var take_money_out = $(QWeb.render('TakeMoneyOut'));

			put_money_in.click(function(){
				msg_show_put_money_in = "";
				msg_show_put_money_in += "<script>" +
											"$('.class_reason').focus();" +
											"$('input').keypress(function(e) {" +
												"if(e.which == 13) {" +
													"$('.button.ok').click();" +
												"}" +
												"else{" +
													"$('.class_amount').keypress(function(event) {" +
														"if(event.which == 8 || event.keyCode == 37 || event.keyCode == 39 || event.keyCode == 46){" +
															"return true;" +
														"}else if" +
															"((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)){" +
																"event.preventDefault();" +
															"}" +
														"});"+
												"}"+
											"});" +
										"</script>" +
										"<div class='main_msg'>" +
											"<span class='sub_content'>" +
												"<table id='tbl_css'>" +
													"<tr>" +
														"<td style='font-size:15px;'>Motivo</td>" +
														"<td><input class='class_reason' type='text' name='txt_reason'></td>" +
													"</tr>" +
													"<tr>" +
														"<td style='font-size:15px;'>Monto</td>" +
														"<td><input class='class_amount' type='text' name='txt_amount'></td>" +
													"</tr>" +
												"</table>" +
											"</spna>" +
										"</div>";
				self.pos_widget.screen_selector.show_popup('custom_dialog_box_put_money_in',{msg_show_put_money_in : msg_show_put_money_in});
			});
			put_money_in.appendTo(this.$('.control-buttons'));
			this.$('.control-buttons').removeClass('oe_hidden');

			take_money_out.click(function(){
				msg_show_take_money_out = "";
				msg_show_take_money_out += "<script>" +
												"$('.class_reason').focus();" +
												"$('input').keypress(function(e) {" +
													"if(e.which == 13) {" +
														"$('.button.ok').click();" +
													"}" +
													"else{" +
													"$('.class_amount').keypress(function(event) {" +
														"if(event.which == 8 || event.keyCode == 37 || event.keyCode == 39 || event.keyCode == 46){" +
															"return true;" +
														"}else if" +
															"((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)){" +
																"event.preventDefault();" +
															"}" +
														"});"+
												"}"+
												"});" +
											"</script>" +
											"<div class='main_msg'>" +
												"<span class='sub_content'>" +
													"<table id='tbl_css'>" +
														"<tr>" +
															"<td style='font-size:15px;'>Motivo</td>" +
															"<td><input class='class_reason' type='text' name='txt_reason'></td>" +
														"</tr>" +
														"<tr>" +
															"<td style='font-size:15px;'>Monto</td>" +
															"<td><input class='class_amount' type='text' name='txt_amount'></td>" +
														"</tr>" +
													"</table>" +
												"</spna>" +
											"</div>";
				self.pos_widget.screen_selector.show_popup('custom_dialog_box_take_money_out',{msg_show_take_money_out : msg_show_take_money_out});
			});
			take_money_out.appendTo(this.$('.control-buttons'));
			this.$('.control-buttons').removeClass('oe_hidden');
		},
	});

	module.custom_dialog_box_put_money_in = instance.point_of_sale.PopUpWidget.extend({
		template : 'CustomPopupPutMoneyIn',
		show : function(options) {
			var self = this;
			var users = self.pos.users;
			this.msg_show_put_money_in = options.msg_show_put_money_in || "";
			this._super();
			this.renderElement();
			this.$('.button.ok').click(function() {

				var name = $('.class_reason').val();
				var amount = $('.class_amount').val();
				var session_id = self.pos.pos_session.id;

				if(!name || !amount){
					alert("Please Fill All Fields.")
				} else
				{
					var model = new instance.web.Model("pos.session"); 
					model.call("put_money_in", 
						[name,amount,session_id], 
						{context: new instance.web.CompoundContext()}).then(function(result) {
							if(result['error']){
								alert(result['error']);
							}
						}).fail(function (error, event){
					        if(error.code === -32098) {
					        	alert("Server closed...");
					        	event.preventDefault();
				           }
				       });
					self.pos_widget.screen_selector.close_popup();
				}
			});

			this.$('.button.cancel').click(function() {
				self.pos_widget.screen_selector.close_popup();
			});
		},
	});

	module.custom_dialog_box_take_money_out = instance.point_of_sale.PopUpWidget.extend({
		template : 'CustomPopupTakeMoneyOut',
		show : function(options) {
			var self = this;
			var users = self.pos.users;
			this.msg_show_take_money_out = options.msg_show_take_money_out || "";
			this._super();
			this.renderElement();
			this.$('.button.ok').click(function() {

				var name = $('.class_reason').val();
				var amount = $('.class_amount').val();
				var session_id = self.pos.pos_session.id;

				if(!name || !amount){
					alert("Please Fill All Fields.")
				} else
				{
					var model = new instance.web.Model("pos.session"); 
					model.call("take_money_out", 
						[name,amount,session_id], 
						{context: new instance.web.CompoundContext()}).then(function(result) {
							if(result['error']){
								alert(result['error']);
							}
						}).fail(function (error, event){
					        if(error.code === -32098) {
					        	alert("Server closed...")
					        	event.preventDefault();
				           }
				       });
					self.pos_widget.screen_selector.close_popup();
				}
			});

			this.$('.button.cancel').click(function() {
				self.pos_widget.screen_selector.close_popup();
			});
		},
	});
}