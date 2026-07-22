import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import generate_dataset


def test_enterprise_dataset_generation(tmp_path):
    stats = generate_dataset.generate_enterprise_dataset(output_root=tmp_path)

    assert stats["assets"] >= 25
    assert stats["components"] >= 250
    assert stats["error_codes"] >= 100
    assert stats["sops"] >= 75
    assert stats["maintenance_logs"] >= 5000
    assert stats["incident_reports"] >= 500
    assert stats["failure_chains"] >= 300
    assert stats["configuration_profiles"] >= 300
    assert stats["ocr_images"] >= 300

    knowledge_dir = tmp_path / "knowledge_base"
    assert (knowledge_dir / "assets").exists()
    assert (tmp_path / "logs" / "maintenance_logs.json").exists()
    assert (tmp_path / "incident_reports").exists()
