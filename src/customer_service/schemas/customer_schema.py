from marshmallow import Schema, fields, validate


class CustomerSchema(Schema):
    """
    Schema for Customer model with comprehensive business rules and EDI configuration
    """
    
    # General
    customer_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    customer_no = fields.Str(
        required=True,
        validate=validate.Length(max=10)
    )
    name = fields.Str(
        allow_none=True,
        validate=validate.Length(max=35)
    )
    explicit_ext_ref = fields.Str(
        allow_none=True,
        validate=validate.Length(max=20)
    )
    abn = fields.Str(
        allow_none=True,
        validate=validate.Length(max=14)
    )
    order_no_recycle_days = fields.Int(allow_none=True)
    shipment_days = fields.Str(
        allow_none=True,
        validate=validate.Length(max=8)
    )
    cancel_order_days = fields.Int(allow_none=True)
    gtin_interpretation = fields.Int(allow_none=True)
    retailer_customisation_format = fields.Int(allow_none=True)
    share_retailer_values = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    
    # Validation Flags
    perform_retailer_validation = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    perform_trade_units_validation = fields.Int(
        load_default=0,
        validate=validate.OneOf([0, 1])
    )
    perform_pack_sizes_validation = fields.Int(
        load_default=0,
        validate=validate.OneOf([0, 1])
    )
    perform_pallets_validation = fields.Int(
        load_default=0,
        validate=validate.OneOf([0, 1])
    )
    
    # Order Flags
    allow_change_order = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_back_order = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_delivery_dates_change = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_part_shipment = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_over_shipment = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_reject_order = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_allowances = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_pack_size_change = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # Picking Flags
    allow_hand_pick = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_over_pick = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_pick_by_prod_wo_scan = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    force_price_basis_to_one = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    include_tax_for_ansi_orders = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_repetitive_nad = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_auto_create_ratio_pack = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # EDI
    edi_address = fields.Str(
        allow_none=True,
        validate=validate.Length(max=30)
    )
    gs02_address = fields.Str(
        allow_none=True,
        validate=validate.Length(max=15)
    )
    gs03_address = fields.Str(
        allow_none=True,
        validate=validate.Length(max=15)
    )
    rpo_gs03_address = fields.Str(
        allow_none=True,
        validate=validate.Length(max=15)
    )
    send_method_key = fields.Str(
        allow_none=True,
        validate=validate.Length(max=8)
    )
    message_release_number = fields.Str(
        allow_none=True,
        validate=validate.Length(max=12)
    )
    x12_line_terminator = fields.Str(
        allow_none=True,
        validate=validate.Length(max=2)
    )
    user_must_accept_order_change = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    order_change_is_whole_order = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    interpret_dts_as_dts = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    d96a_include_tax = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_updated_poi_import = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # Prices
    prices_as_per_locations = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    contract_price_grp_key = fields.Int(allow_none=True)
    promo_price_grp_key = fields.Int(allow_none=True)
    retail_price_grp_key = fields.Int(allow_none=True)
    check_order_prices = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    check_tax_rate = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    validate_tax = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    edit_tax_rate = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    edit_cost_price = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    fetch_price_from_price_table = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # Labels
    shipment_labelling = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    scm_label_format = fields.Str(
        allow_none=True,
        validate=validate.Length(max=20)
    )
    price_label_format = fields.Str(
        allow_none=True,
        validate=validate.Length(max=20)
    )
    print_price_labels = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    blank_page_between_products = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    print_ge_key_code = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    print_dept_no_on_labels = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    qr_from_contract_no = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # RPO (Replenishment Purchase Order)
    rpo_format = fields.Int(allow_none=True)
    rpo_seq_no_start = fields.Int(allow_none=True)
    rpo_seq_no_end = fields.Int(allow_none=True)
    rpo_aper_ack_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    rpo_fnack_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # FnA (Functional Acknowledgement)
    create_fnack_when = fields.Int(allow_none=True)
    create_dts_fnack = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    create_dc_fnack = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    create_cross_dock_fnack = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    fa_format = fields.Int(allow_none=True)
    
    # POA (Purchase Order Acknowledgement)
    create_prod_poa_when = fields.Int(allow_none=True)
    create_test_poa_when = fields.Int(allow_none=True)
    poa_format = fields.Int(allow_none=True)
    poa_generate_auto = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    rejection_comments_required = fields.Int(
        load_default=0,
        validate=validate.OneOf([0, 1])
    )
    change_comments_required = fields.Int(
        load_default=0,
        validate=validate.OneOf([0, 1])
    )
    block_changes_after_sending_poa = fields.Int(
        load_default=0,
        validate=validate.OneOf([0, 1])
    )
    poa_fnack_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    poa_aper_ack_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_del_dates_change_at_line_level = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # ASN (Advanced Shipment Notice)
    create_prod_asn_when = fields.Int(allow_none=True)
    create_test_asn_when = fields.Int(allow_none=True)
    allow_dc_asn = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    allow_cross_dock_asn = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    allow_store_asn = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    multiple_dts_asns = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    asn_fna_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    asn_format = fields.Int(allow_none=True)
    asn_aper_ack_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    user_supplied_shipment_no = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    include_product_gross_weight = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    
    # INVOICE
    collect_data_from_split_orders = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_dc_invoice = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    allow_cross_dock_invoice = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    allow_dts_invoice = fields.Int(
        load_default=1,
        validate=validate.OneOf([0, 1])
    )
    multiple_dts_invoices = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_credit_note = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    invoice_aper_ack_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    invoice_fnack_req = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    invoice_format = fields.Int(allow_none=True)
    payment_due_days = fields.Int(allow_none=True)
    invoice_generate_auto = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    invoice_payment_terms = fields.Int(allow_none=True)
    invoice_payment_conditions_charges = fields.Int(
        load_default=0,
        validate=validate.OneOf([0, 1])
    )
    debtors_account_no = fields.Str(
        allow_none=True,
        validate=validate.Length(max=70)
    )
    allow_discounts = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    allow_surcharges = fields.Int(
        allow_none=True,
        validate=validate.OneOf([0, 1])
    )
    discount_method = fields.Int(load_default=0)
    surcharge_method = fields.Int(load_default=0)
