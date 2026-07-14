import re
from pathlib import Path

from PIL import Image


class PDFGenerator:
    _FRAME_FOLDER_NAME: Path = Path("outputs/frames")
    _OUTPUT_FOLDER_PATH_NAME: Path = Path("outputs/pdf")

    @staticmethod
    def _get_image_files() -> list[Path]:
        """Retrieve and chronologically short all PNG files within the frames directory."""
        folder_path = PDFGenerator._FRAME_FOLDER_NAME
        if not folder_path.exists():
            raise FileNotFoundError("\n\nFile not found!", {folder_path.resolve()})

        all_files = list(folder_path.glob("*.png"))
        if not all_files:
            raise ValueError(f"No PNG files found in {folder_path.resolve()}")

        # Sort files in chronological order (01, 02. ...)
        sorted_files = sorted(
            all_files,
            key=lambda x: [
                int(c) if c.isdigit() else c for c in re.split(r"(\d+)", x.name)
            ],
        )
        return sorted_files

    @staticmethod
    def _convert_rgb(img: Image.Image) -> Image.Image:
        """Convert RGBA to RGB format for compatibility."""
        if img.mode in ("RGBA", "P"):
            return img.img.convert("RGB")
        return img

    def get_pdf(
        self,
        pdf_name: str = "video_note",
    ) -> None:
        """Compile the sorted frames into a single PDF."""
        sorted_files = self._get_image_files()

        first_img = Image.open(sorted_files[0])
        first_img = self._convert_rgb(first_img)

        frame_list: list[Image.Image] = []
        for file_path in sorted_files[1:]:
            img = Image.open(file_path)
            img = self._convert_rgb(img)
            frame_list.append(img)

        output_path = Path(PDFGenerator._OUTPUT_FOLDER_PATH_NAME)
        output_path.mkdir(parents=True, exist_ok=True)

        output_pdf_path = output_path / f"{pdf_name}.pdf"

        first_img.save(output_pdf_path, save_all=True, append_images=frame_list)
        print(f"\nPDF saved successfully! \nFile Path:{output_pdf_path}")


if __name__ == "__main__":
    generator = PDFGenerator()
    generator.get_pdf()
