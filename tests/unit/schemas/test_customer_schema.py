"""
Tests for customer_schema.py
"""
import pytest
from marshmallow import ValidationError
from customer_service.schemas.customer_schema import CustomerSchema


class TestCustomerSchemaValidation:
    """Test CustomerSchema validation"""
    
    def setup_method(self):
        """Setup for each test"""
        self.schema = CustomerSchema()
    
    def test_valid_customer_data(self, sample_customer_data):
        """Test schema accepts valid customer data"""
        result = self.schema.load(sample_customer_data)
        assert result["customer_no"] == "CUST001"
        assert result["name"] == "Test Customer"
    
    def test_missing_required_customer_no(self):
        """Test schema rejects missing customer_no"""
        data = {"name": "Test Customer"}
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "customer_no" in exc_info.value.messages
    
    def test_customer_no_max_length(self):
        """Test customer_no maximum length validation"""
        data = {"customer_no": "A" * 11}  # Exceeds max length of 10
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "customer_no" in exc_info.value.messages
    
    def test_customer_no_valid_length(self, sample_customer_data):
        """Test customer_no with valid length"""
        data = {"customer_no": "CUST12345"}
        result = self.schema.load(data)
        assert result["customer_no"] == "CUST12345"
    
    def test_name_max_length(self):
        """Test name maximum length validation"""
        data = {"customer_no": "CUST001", "name": "A" * 36}  # Exceeds max length of 35
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "name" in exc_info.value.messages
    
    def test_name_allow_none(self):
        """Test name field allows None"""
        data = {"customer_no": "CUST001", "name": None}
        result = self.schema.load(data)
        assert result["name"] is None
    
    def test_explicit_ext_ref_max_length(self):
        """Test explicit_ext_ref maximum length"""
        data = {"customer_no": "CUST001", "explicit_ext_ref": "A" * 21}  # Exceeds max of 20
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "explicit_ext_ref" in exc_info.value.messages
    
    def test_abn_max_length(self):
        """Test ABN maximum length"""
        data = {"customer_no": "CUST001", "abn": "A" * 15}  # Exceeds max of 14
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "abn" in exc_info.value.messages
    
    def test_shipment_days_max_length(self):
        """Test shipment_days maximum length"""
        data = {"customer_no": "CUST001", "shipment_days": "A" * 9}  # Exceeds max of 8
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "shipment_days" in exc_info.value.messages


class TestCustomerSchemaFlagValidation:
    """Test validation flag fields"""
    
    def setup_method(self):
        """Setup for each test"""
        self.schema = CustomerSchema()
    
    def test_share_retailer_values_default(self):
        """Test share_retailer_values defaults to 1"""
        result = self.schema.load({"customer_no": "CUST001"})
        assert result["share_retailer_values"] == 1
    
    def test_share_retailer_values_valid_values(self):
        """Test share_retailer_values accepts 0 and 1"""
        for value in [0, 1]:
            result = self.schema.load({"customer_no": "CUST001", "share_retailer_values": value})
            assert result["share_retailer_values"] == value
    
    def test_share_retailer_values_invalid(self):
        """Test share_retailer_values rejects invalid values"""
        data = {"customer_no": "CUST001", "share_retailer_values": 2}
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "share_retailer_values" in exc_info.value.messages
    
    def test_perform_retailer_validation_default(self):
        """Test perform_retailer_validation defaults to 1"""
        result = self.schema.load({"customer_no": "CUST001"})
        assert result["perform_retailer_validation"] == 1
    
    def test_perform_trade_units_validation_default(self):
        """Test perform_trade_units_validation defaults to 0"""
        result = self.schema.load({"customer_no": "CUST001"})
        assert result["perform_trade_units_validation"] == 0
    
    def test_perform_pack_sizes_validation_default(self):
        """Test perform_pack_sizes_validation defaults to 0"""
        result = self.schema.load({"customer_no": "CUST001"})
        assert result["perform_pack_sizes_validation"] == 0
    
    def test_perform_pallets_validation_default(self):
        """Test perform_pallets_validation defaults to 0"""
        result = self.schema.load({"customer_no": "CUST001"})
        assert result["perform_pallets_validation"] == 0
    
    def test_validation_flags_accept_none(self):
        """Test order/picking flags accept None"""
        data = {
            "customer_no": "CUST001",
            "allow_change_order": None,
            "allow_back_order": None
        }
        result = self.schema.load(data)
        assert result.get("allow_change_order") is None
        assert result.get("allow_back_order") is None


class TestCustomerSchemaOrderFlags:
    """Test order flag field validation"""
    
    def setup_method(self):
        """Setup for each test"""
        self.schema = CustomerSchema()
    
    def test_order_flags_valid_values(self):
        """Test order flags accept 0 and 1"""
        flags = [
            "allow_change_order", "allow_back_order", "allow_delivery_dates_change",
            "allow_part_shipment", "allow_over_shipment", "allow_reject_order",
            "allow_allowances", "allow_pack_size_change"
        ]
        
        for flag in flags:
            for value in [0, 1]:
                result = self.schema.load({"customer_no": "CUST001", flag: value})
                assert result[flag] == value
    
    def test_order_flags_invalid_values(self):
        """Test order flags reject invalid values"""
        data = {"customer_no": "CUST001", "allow_change_order": 2}
        with pytest.raises(ValidationError):
            self.schema.load(data)


class TestCustomerSchemaPickingFlags:
    """Test picking flag field validation"""
    
    def setup_method(self):
        """Setup for each test"""
        self.schema = CustomerSchema()
    
    def test_picking_flags_valid_values(self):
        """Test picking flags accept 0 and 1"""
        flags = [
            "allow_hand_pick", "allow_over_pick", "allow_pick_by_prod_wo_scan"
        ]
        
        for flag in flags:
            for value in [0, 1]:
                result = self.schema.load({"customer_no": "CUST001", flag: value})
                assert result[flag] == value


class TestCustomerSchemaSerialization:
    """Test schema serialization (dump)"""
    
    def setup_method(self):
        """Setup for each test"""
        self.schema = CustomerSchema()
    
    def test_dump_only_fields(self):
        """Test that customer_id and user_id are dump_only (rejected on load)"""
        data = {
            "customer_no": "CUST001",
            "customer_id": 999,
            "user_id": 999
        }
        # Loading dump_only fields should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "customer_id" in str(exc_info.value) or "user_id" in str(exc_info.value)


class TestCustomerSchemaPartialUpdate:
    """Test schema with partial=True"""
    
    def test_partial_schema_no_required_fields(self):
        """Test that partial schema doesn't require customer_no"""
        schema = CustomerSchema(partial=True)
        result = schema.load({"name": "Updated Name"})
        assert result["name"] == "Updated Name"
    
    def test_partial_schema_with_customer_no(self):
        """Test partial schema accepts customer_no"""
        schema = CustomerSchema(partial=True)
        result = schema.load({"customer_no": "CUST002", "name": "Updated"})
        assert result["customer_no"] == "CUST002"
        assert result["name"] == "Updated"


class TestCustomerSchemaIntegration:
    """Integration tests for schema"""
    
    def test_load_and_dump_round_trip(self, sample_customer_data):
        """Test that data can be loaded and dumped back"""
        schema = CustomerSchema()
        loaded = schema.load(sample_customer_data)
        assert loaded["customer_no"] == sample_customer_data["customer_no"]
    
    def test_schema_with_many(self):
        """Test schema can handle many=True"""
        schema = CustomerSchema(many=True)
        data = [
            {"customer_no": "CUST001", "name": "Customer 1"},
            {"customer_no": "CUST002", "name": "Customer 2"}
        ]
        result = schema.load(data)
        assert len(result) == 2
        assert result[0]["customer_no"] == "CUST001"
