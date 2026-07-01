from customer_service.extentions.db import db

# docker exec -it customer-service bash
# python -m alembic revision --autogenerate -m "Added new column"
# python -m alembic upgrade head


class CustomerModel(db.Model):
    __tablename__ = "customers"

    __table_args__ = (
        db.UniqueConstraint("user_id", "customer_no", name="uq_user_customer_no"),
    )
    
    user_id = db.Column(db.Integer, nullable=False, index=True)
    # General
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_no = db.Column(db.String(10), nullable=False, unique=True, index=True)
    name = db.Column(db.String(35))
    explicit_ext_ref = db.Column(db.String(20))
    abn = db.Column(db.String(14))
    order_no_recycle_days = db.Column(db.SmallInteger)
    shipment_days = db.Column(db.String(8))
    cancel_order_days = db.Column(db.SmallInteger)
    gtin_interpretation = db.Column(db.Integer)
    retailer_customisation_format = db.Column(db.SmallInteger)
    share_retailer_values = db.Column(db.SmallInteger, nullable=False, default=1)

    # Validation Flags
    perform_retailer_validation = db.Column(db.SmallInteger, nullable=False, default=1)
    perform_trade_units_validation = db.Column(db.SmallInteger, nullable=False, default=0)
    perform_pack_sizes_validation = db.Column(db.SmallInteger, nullable=False, default=0)
    perform_pallets_validation = db.Column(db.SmallInteger, nullable=False, default=0)

    # Order Flags
    allow_change_order = db.Column(db.SmallInteger)
    allow_back_order = db.Column(db.SmallInteger)
    allow_delivery_dates_change = db.Column(db.SmallInteger)
    allow_part_shipment = db.Column(db.SmallInteger)
    allow_over_shipment = db.Column(db.SmallInteger)
    allow_reject_order = db.Column(db.SmallInteger)
    allow_allowances = db.Column(db.SmallInteger)
    allow_pack_size_change = db.Column(db.SmallInteger)

    # Picking Flags
    allow_hand_pick = db.Column(db.SmallInteger)
    allow_over_pick = db.Column(db.SmallInteger)
    allow_pick_by_prod_wo_scan = db.Column(db.SmallInteger)
    force_price_basis_to_one = db.Column(db.SmallInteger)
    include_tax_for_ansi_orders = db.Column(db.SmallInteger)
    allow_repetitive_nad = db.Column(db.SmallInteger)
    allow_auto_create_ratio_pack = db.Column(db.SmallInteger)

    # EDI
    edi_address = db.Column(db.String(30))
    gs02_address = db.Column(db.String(15))
    gs03_address = db.Column(db.String(15))
    rpo_gs03_address = db.Column(db.String(15))
    send_method_key = db.Column(db.String(8))
    message_release_number = db.Column(db.String(12))
    x12_line_terminator = db.Column(db.String(2))
    user_must_accept_order_change = db.Column(db.SmallInteger)
    order_change_is_whole_order = db.Column(db.SmallInteger)
    interpret_dts_as_dts = db.Column(db.SmallInteger)
    d96a_include_tax = db.Column(db.SmallInteger)
    allow_updated_poi_import = db.Column(db.SmallInteger)

    # Prices
    prices_as_per_locations = db.Column(db.SmallInteger)
    contract_price_grp_key = db.Column(db.SmallInteger)
    promo_price_grp_key = db.Column(db.SmallInteger)
    retail_price_grp_key = db.Column(db.SmallInteger)
    check_order_prices = db.Column(db.SmallInteger)
    check_tax_rate = db.Column(db.SmallInteger)
    validate_tax = db.Column(db.SmallInteger)
    edit_tax_rate = db.Column(db.SmallInteger)
    edit_cost_price = db.Column(db.SmallInteger)
    fetch_price_from_price_table = db.Column(db.SmallInteger)

    # Labels
    shipment_labelling = db.Column(db.SmallInteger)
    scm_label_format = db.Column(db.String(20))
    price_label_format = db.Column(db.String(20))
    print_price_labels = db.Column(db.SmallInteger)
    blank_page_between_products = db.Column(db.SmallInteger)
    print_ge_key_code = db.Column(db.SmallInteger)
    print_dept_no_on_labels = db.Column(db.SmallInteger)
    qr_from_contract_no = db.Column(db.SmallInteger)

    # RPO (Replenishment Purchase Order)
    rpo_format = db.Column(db.SmallInteger)
    rpo_seq_no_start = db.Column(db.Integer)
    rpo_seq_no_end = db.Column(db.Integer)
    rpo_aper_ack_req = db.Column(db.SmallInteger)
    rpo_fnack_req = db.Column(db.SmallInteger)

    # FnA (Functional Acknowledgement)
    create_fnack_when = db.Column(db.SmallInteger)
    create_dts_fnack = db.Column(db.SmallInteger, nullable=False, default=1)
    create_dc_fnack = db.Column(db.SmallInteger, nullable=False, default=1)
    create_cross_dock_fnack = db.Column(db.SmallInteger, nullable=False, default=1)
    fa_format = db.Column(db.Integer)

    # POA (Purchase Order Acknowledgement)
    create_prod_poa_when = db.Column(db.SmallInteger)
    create_test_poa_when = db.Column(db.SmallInteger)
    poa_format = db.Column(db.SmallInteger)
    poa_generate_auto = db.Column(db.SmallInteger)
    rejection_comments_required = db.Column(db.SmallInteger, nullable=False, default=0)
    change_comments_required = db.Column(db.SmallInteger, nullable=False, default=0)
    block_changes_after_sending_poa = db.Column(db.SmallInteger, nullable=False, default=0)
    poa_fnack_req = db.Column(db.SmallInteger)
    poa_aper_ack_req = db.Column(db.SmallInteger)
    allow_del_dates_change_at_line_level = db.Column(db.SmallInteger)

    # ASN (Advanced Shipment Notice)
    create_prod_asn_when = db.Column(db.SmallInteger)
    create_test_asn_when = db.Column(db.SmallInteger)
    allow_dc_asn = db.Column(db.SmallInteger, nullable=False, default=1)
    allow_cross_dock_asn = db.Column(db.SmallInteger, nullable=False, default=1)
    allow_store_asn = db.Column(db.SmallInteger)
    multiple_dts_asns = db.Column(db.SmallInteger)
    asn_fna_req = db.Column(db.SmallInteger)
    asn_format = db.Column(db.Integer)
    asn_aper_ack_req = db.Column(db.SmallInteger)
    user_supplied_shipment_no = db.Column(db.SmallInteger)
    include_product_gross_weight = db.Column(db.SmallInteger)

    # INVOICE
    collect_data_from_split_orders = db.Column(db.SmallInteger)
    allow_dc_invoice = db.Column(db.SmallInteger, nullable=False, default=1)
    allow_cross_dock_invoice = db.Column(db.SmallInteger, nullable=False, default=1)
    allow_dts_invoice = db.Column(db.SmallInteger, nullable=False, default=1)
    multiple_dts_invoices = db.Column(db.SmallInteger)
    allow_credit_note = db.Column(db.SmallInteger)
    invoice_aper_ack_req = db.Column(db.SmallInteger)
    invoice_fnack_req = db.Column(db.SmallInteger)
    invoice_format = db.Column(db.SmallInteger)
    payment_due_days = db.Column(db.SmallInteger)
    invoice_generate_auto = db.Column(db.SmallInteger)
    invoice_payment_terms = db.Column(db.SmallInteger)
    invoice_payment_conditions_charges = db.Column(db.SmallInteger, nullable=False, default=0)
    debtors_account_no = db.Column(db.String(70))
    allow_discounts = db.Column(db.SmallInteger)
    allow_surcharges = db.Column(db.SmallInteger)
    discount_method = db.Column(db.SmallInteger, default=0)
    surcharge_method = db.Column(db.SmallInteger, default=0)

    def __repr__(self):
        return f"<CustomerModel(customer_id={self.customer_id}, customer_no='{self.customer_no}', name='{self.name}')>"
