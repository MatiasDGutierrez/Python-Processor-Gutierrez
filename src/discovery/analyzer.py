import os
from typing import List, Dict
import pandas as pd
from PyPDF2 import PdfReader

class FileAnalyzer:
    def __init__(self, raw_data_path: str):
        self.raw_data_path = raw_data_path

    def list_files(self) -> List[str]:
        return [f for f in os.listdir(self.raw_data_path) if os.path.isfile(os.path.join(self.raw_data_path, f))]

    def analyze_all(self) -> List[Dict]:
        results = []
        for filename in self.list_files():
            file_path = os.path.join(self.raw_data_path, filename)
            ext = os.path.splitext(filename)[1].lower()
            analysis = {
                "filename": filename,
                "extension": ext,
                "type": self._get_type(ext),
                "details": self._get_details(file_path, ext)
            }
            results.append(analysis)
        return results

    def _get_type(self, ext: str) -> str:
        if ext in ['.xlsx', '.xls', '.csv']:
            return "Excel/Structured"
        elif ext == '.pdf':
            return "PDF"
        else:
            return "Unknown"

    def _get_details(self, file_path: str, ext: str) -> Dict:
        try:
            if ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, nrows=1)
                return {"columns": list(df.columns), "sheets": "N/A"} # Could expand to list all sheets
            elif ext == '.pdf':
                reader = PdfReader(file_path)
                return {"pages": len(reader.pages), "metadata": str(reader.metadata)}
            else:
                return {}
        except Exception as e:
            return {"error": str(e)}
