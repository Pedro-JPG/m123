openerp.pos_restaurant_uruguay = function(instance){

    var module = instance.point_of_sale;

    openerp_restaurant_multiprint(instance,module);

    openerp_restaurant_splitbill(instance,module);

    openerp_restaurant_printbill(instance,module);

};
