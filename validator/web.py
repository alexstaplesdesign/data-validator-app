import tempfile
import shutil
import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from validator.runner import run_validation_for_web
from validator.models import FileValidationResult


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Data Validator",
    description="Modern CSV data validation tool with beautiful reporting",
    version="1.0.0"
)

# Setup templates
templates = Jinja2Templates(directory="validator/templates")

# Create reports directory
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


class ValidationResponse(BaseModel):
    """Response model for validation results."""
    success: bool
    message: str
    results: List[dict]
    summary: dict


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Data Validator API is running"}


@app.post("/api/validate", response_model=ValidationResponse)
async def validate_files(files: List[UploadFile] = File(...)):
    """Upload and validate CSV files."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Check file types
    for file in files:
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type: {file.filename}. Only CSV files are allowed."
            )

    results = []
    temp_files = []
    
    try:
        # Create temporary directory for uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            uploaded_files = []
            
            # Save uploaded files to temporary directory
            for file in files:
                file_path = temp_path / file.filename
                with file_path.open("wb") as f:
                    shutil.copyfileobj(file.file, f)
                uploaded_files.append(file_path)
                temp_files.append(file_path)
            
            # Run validation
            validation_results = run_validation_for_web(uploaded_files, REPORTS_DIR)
            
            # Convert results to response format
            total_rows = 0
            total_errors = 0
            total_invalid_rows = 0
            
            for result in validation_results:
                total_rows += result.counts.total_rows
                total_errors += result.counts.validation_error_count
                total_invalid_rows += result.counts.invalid_row_count
                
                results.append({
                    "filename": result.filename,
                    "total_rows": result.counts.total_rows,
                    "invalid_rows": result.counts.invalid_row_count,
                    "validation_errors": result.counts.validation_error_count,
                    "errors": [
                        {
                            "row_number": err.row_number,
                            "field": err.field,
                            "message": err.message
                        }
                        for err in result.errors
                    ]
                })
            
            summary = {
                "total_files": len(validation_results),
                "total_rows": total_rows,
                "total_invalid_rows": total_invalid_rows,
                "total_validation_errors": total_errors,
                "has_errors": total_errors > 0
            }
            
            return ValidationResponse(
                success=True,
                message=f"Validated {len(files)} files successfully",
                results=results,
                summary=summary
            )
    
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@app.get("/api/samples")
async def list_sample_files():
    """List available sample CSV files for download."""
    try:
        sample_files = []
        data_dir = Path("data")
        
        if data_dir.exists():
            for file_path in data_dir.glob("sample_*.csv"):
                # Read first few lines to show preview
                try:
                    with file_path.open("r", encoding="utf-8") as f:
                        lines = f.readlines()
                        preview = "".join(lines[:4])  # Header + 3 data rows
                        
                    sample_files.append({
                        "name": file_path.name,
                        "description": get_sample_description(file_path.name),
                        "size": file_path.stat().st_size,
                        "preview": preview,
                        "download_url": f"/api/samples/download/{file_path.name}"
                    })
                except Exception as e:
                    logger.warning(f"Could not read sample file {file_path.name}: {e}")
        
        return {"samples": sample_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list samples: {str(e)}")


@app.get("/api/samples/download/{filename}")
async def download_sample_file(filename: str):
    """Download a specific sample CSV file."""
    if not filename.startswith("sample_") or not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid sample file name")
    
    file_path = Path("data") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Sample file not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )


def get_sample_description(filename: str) -> str:
    """Get description for sample files."""
    descriptions = {
        "sample_perfect.csv": "✅ Perfect data - All records pass validation (8 records)",
        "sample_mixed_errors.csv": "⚠️ Mixed errors - Showcases all validation rules (10 records)", 
        "sample_large_dataset.csv": "📈 Large dataset - Performance testing (20 records)",
        "sample_edge_cases.csv": "🔍 Edge cases - Boundary conditions and special characters",
        "sample_critical_errors.csv": "❌ Critical errors - Worst-case scenarios",
        "sample_international.csv": "🌍 International - Unicode names and characters",
        "customers_valid.csv": "✅ Simple valid example (5 records)",
        "customers_with_errors.csv": "⚠️ Example with common errors",
        "customers_bad_header.csv": "❌ Missing required columns (for testing)"
    }
    return descriptions.get(filename, "📄 Sample CSV file for testing")


@app.get("/api/reports")
async def list_reports():
    """List available validation reports."""
    try:
        reports = []
        if REPORTS_DIR.exists():
            for file_path in REPORTS_DIR.iterdir():
                if file_path.is_file():
                    reports.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime
                    })
        
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list reports: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Data Validator Web Server...")
    print("📊 Open http://localhost:8000 in your browser")
    uvicorn.run(
        "validator.web:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )