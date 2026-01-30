# 📊 Sample Data Files for Testing

## 🎯 **Test File Descriptions**

### 1. `sample_perfect.csv` ✅
- **Purpose:** Perfect validation test
- **Content:** 8 completely valid customer records
- **Expected Result:** ✅ No errors, all green status
- **Use Case:** Verify the validator works correctly with good data

### 2. `sample_mixed_errors.csv` ⚠️
- **Purpose:** Comprehensive error showcase
- **Errors Include:**
  - Customer ID = 0 (must be > 0)
  - Missing full name (empty field)
  - Invalid email format (missing @, ending with @)
  - Invalid customer ID (non-numeric: "abc")
  - Name too short ("F" - must be 2-80 chars)
  - Name too long (exceeds 80 characters)
  - Future signup date (2030)
  - Invalid date format ("not-a-date")
- **Expected Result:** ❌ Multiple validation errors
- **Use Case:** Test all validation rules

### 3. `sample_large_dataset.csv` 📈
- **Purpose:** Performance testing
- **Content:** 20 valid customer records
- **Expected Result:** ✅ No errors, good performance
- **Use Case:** Test handling of larger files

### 4. `sample_edge_cases.csv` 🔍
- **Purpose:** Boundary condition testing
- **Content:**
  - Very large customer ID (999999)
  - Minimum name length (2 chars: "Ab")
  - Special characters (apostrophes, hyphens)
  - Unicode characters (José, 李小明)
  - Very old date (1900)
  - Date on boundary (2025-12-31)
- **Expected Result:** ✅ Should pass validation
- **Use Case:** Test edge cases and internationalization

### 5. `sample_critical_errors.csv` ❌
- **Purpose:** Worst-case scenario testing
- **Content:**
  - Completely empty rows
  - Multiple field violations per row
  - Negative customer IDs
  - Invalid date (Feb 30th)
  - Whitespace-only fields
- **Expected Result:** ❌ Many critical errors
- **Use Case:** Test error handling robustness

### 6. `sample_international.csv` 🌍
- **Purpose:** International character support
- **Content:**
  - Names in French, Japanese, Spanish, Russian, Arabic, Norwegian, Greek, Hindi
  - Unicode characters and diacritics
  - Various international email domains
- **Expected Result:** ✅ Should pass validation
- **Use Case:** Test Unicode and international support

## 🧪 **How to Test**

### Via Web Interface:
1. Open http://localhost:8000
2. Drag and drop any of these files into the upload zone
3. Click "Validate Files"
4. View the beautiful results with charts and error tables

### Via CLI:
```bash
# Test perfect file
python -m validator.cli --input data --reports reports --pattern "sample_perfect.csv"

# Test mixed errors
python -m validator.cli --input data --reports reports --pattern "sample_mixed_errors.csv" --failOnError true

# Test all samples
python -m validator.cli --input data --reports reports --pattern "sample_*.csv"
```

## 🎨 **Expected Web Interface Results**

- **Green Cards:** Valid files with ✅ checkmarks
- **Red Cards:** Files with errors showing ❌ symbols
- **Interactive Tables:** Click through error details
- **Statistics Dashboard:** Real-time counts and percentages
- **Beautiful Charts:** Visual representation of data quality

Test these files to see the full power of your data validation application! 🚀