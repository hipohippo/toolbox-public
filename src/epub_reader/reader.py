import json
import os
import sys

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class HighlightingPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlights = []

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # Handle messages from JavaScript
        if message.startswith("HIGHLIGHT:"):
            self.highlights.append(message.replace("HIGHLIGHT:", ""))


class EPUBReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.book = None
        self.current_chapter = 0
        self.chapters = []
        self.highlights = {}
        self.settings = QSettings("EPUBReader", "EPUBReader")

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("EPUB Reader")
        self.setGeometry(100, 100, 1000, 800)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Open file action
        open_action = QAction("Open EPUB", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        # Font size controls
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Font Size:"))
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setMinimum(50)
        self.font_slider.setMaximum(200)
        self.font_slider.setValue(100)
        self.font_slider.setTickInterval(10)
        self.font_slider.setTickPosition(QSlider.TicksBelow)
        self.font_slider.valueChanged.connect(self.change_font_size)
        toolbar.addWidget(self.font_slider)

        # Highlight button
        highlight_btn = QPushButton("Highlight Selection")
        highlight_btn.clicked.connect(self.highlight_selection)
        toolbar.addWidget(highlight_btn)

        # Export highlights button
        export_btn = QPushButton("Export Highlights")
        export_btn.clicked.connect(self.export_highlights)
        toolbar.addWidget(export_btn)

        # Navigation buttons
        prev_btn = QPushButton("Previous")
        prev_btn.clicked.connect(self.prev_chapter)
        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.next_chapter)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(next_btn)

        # Web view for displaying EPUB content
        self.web_view = QWebEngineView()
        self.page = HighlightingPage(self.web_view)
        self.web_view.setPage(self.page)

        # Add widgets to layout
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.web_view)

        self.statusBar().showMessage("Ready")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open EPUB File", "", "EPUB Files (*.epub)"
        )

        if file_path:
            self.load_epub(file_path)

    def load_epub(self, file_path):
        try:
            self.book = epub.read_epub(file_path)
            self.chapters = []

            # Extract chapters
            for item in self.book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    self.chapters.append(item)

            # Load highlights if they exist
            self.highlights = {}
            highlight_path = os.path.join(
                os.path.dirname(file_path), os.path.basename(file_path) + ".highlights"
            )
            if os.path.exists(highlight_path):
                with open(highlight_path, "r", encoding="utf-8") as f:
                    self.highlights = json.load(f)

            # Load last position
            book_id = os.path.basename(file_path)
            last_position = self.settings.value(f"{book_id}/position", 0, type=int)
            self.current_chapter = min(last_position, len(self.chapters) - 1)

            # Display the chapter
            self.display_chapter()

            self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)}")

        except Exception as e:
            self.statusBar().showMessage(f"Error loading EPUB: {str(e)}")

    def display_chapter(self):
        if not self.book or not self.chapters:
            return

        chapter = self.chapters[self.current_chapter]
        content = chapter.get_content().decode("utf-8")

        # Parse with BeautifulSoup to modify content
        soup = BeautifulSoup(content, "html.parser")

        # Add our custom CSS for highlighting
        style_tag = soup.new_tag("style")
        style_tag.string = """
        .highlighted {
            background-color: yellow;
        }
        """
        if soup.head:
            soup.head.append(style_tag)
        else:
            head_tag = soup.new_tag("head")
            head_tag.append(style_tag)
            soup.insert(0, head_tag)

        # Add JavaScript for handling text selection and highlighting
        script_tag = soup.new_tag("script")
        script_tag.string = """
        document.addEventListener('mouseup', function() {
            var selection = window.getSelection();
            if (selection.toString().length > 0) {
                var range = selection.getRangeAt(0);
                var selectedText = selection.toString();
                console.log("Selected: " + selectedText);
            }
        });
        
        function highlightSelection() {
            var selection = window.getSelection();
            if (selection.toString().length > 0) {
                var range = selection.getRangeAt(0);
                var selectedText = selection.toString();
                
                var span = document.createElement('span');
                span.className = 'highlighted';
                span.textContent = selectedText;
                
                range.deleteContents();
                range.insertNode(span);
                
                // Send the highlighted text to Python
                console.log("HIGHLIGHT:" + selectedText);
            }
        }
        """
        if soup.body:
            soup.body.append(script_tag)

        # Apply existing highlights
        chapter_id = chapter.get_id()
        if chapter_id in self.highlights:
            for highlight_text in self.highlights[chapter_id]:
                # This is a simplified approach - in a real app, you'd need more sophisticated text matching
                text_nodes = soup.find_all(string=lambda text: highlight_text in text)
                for text_node in text_nodes:
                    highlighted_tag = soup.new_tag("span")
                    highlighted_tag["class"] = "highlighted"
                    highlighted_tag.string = highlight_text
                    text_node.replace_with(
                        text_node.replace(highlight_text, str(highlighted_tag))
                    )

        modified_content = str(soup)

        # Load the content into the web view
        self.web_view.setHtml(modified_content)

        # Apply current font size
        self.change_font_size(self.font_slider.value())

        # Save position
        if hasattr(self, "current_file_path"):
            book_id = os.path.basename(self.current_file_path)
            self.settings.setValue(f"{book_id}/position", self.current_chapter)

    def change_font_size(self, value):
        zoom_factor = value / 100.0
        self.web_view.setZoomFactor(zoom_factor)

    def highlight_selection(self):
        self.web_view.page().runJavaScript("highlightSelection();")

        # Store highlights (in a real app, you'd need to handle this more robustly)
        if self.page.highlights and self.chapters:
            chapter_id = self.chapters[self.current_chapter].get_id()
            if chapter_id not in self.highlights:
                self.highlights[chapter_id] = []

            for highlight in self.page.highlights:
                if highlight not in self.highlights[chapter_id]:
                    self.highlights[chapter_id].append(highlight)

            self.page.highlights = []  # Clear after processing

            # Save highlights
            if hasattr(self, "current_file_path"):
                highlight_path = self.current_file_path + ".highlights"
                with open(highlight_path, "w", encoding="utf-8") as f:
                    json.dump(self.highlights, f)

    def export_highlights(self):
        if not self.highlights:
            self.statusBar().showMessage("No highlights to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Highlights", "", "Text Files (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    for chapter_id, highlights in self.highlights.items():
                        # Find chapter title if possible
                        chapter_title = "Chapter"
                        for item in self.book.get_items():
                            if item.get_id() == chapter_id:
                                soup = BeautifulSoup(
                                    item.get_content().decode("utf-8"), "html.parser"
                                )
                                title_tag = soup.find("title")
                                if title_tag:
                                    chapter_title = title_tag.text
                                break

                        f.write(f"=== {chapter_title} ===\n\n")
                        for highlight in highlights:
                            f.write(f"• {highlight}\n\n")

                self.statusBar().showMessage(f"Highlights exported to {file_path}")
            except Exception as e:
                self.statusBar().showMessage(f"Error exporting highlights: {str(e)}")

    def next_chapter(self):
        if self.chapters and self.current_chapter < len(self.chapters) - 1:
            self.current_chapter += 1
            self.display_chapter()

    def prev_chapter(self):
        if self.chapters and self.current_chapter > 0:
            self.current_chapter -= 1
            self.display_chapter()

    def closeEvent(self, event):
        # Save current position before closing
        if hasattr(self, "current_file_path") and self.book:
            book_id = os.path.basename(self.current_file_path)
            self.settings.setValue(f"{book_id}/position", self.current_chapter)
        event.accept()


def main():
    app = QApplication(sys.argv)
    reader = EPUBReader()
    reader.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
