from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QFontDatabase

app = QApplication([])

database = QFontDatabase()
fontTree = QTreeWidget()
fontTree.setColumnCount(2)
fontTree.setHeaderLabels(["Font", "Smooth Sizes"])

for family in database.families():
    familyItem = QTreeWidgetItem(fontTree)
    familyItem.setText(0, family)

    for style in database.styles(family):
        styleItem = QTreeWidgetItem(familyItem)
        styleItem.setText(0, style)

        sizes = ""
        for points in database.smoothSizes(family, style):
            sizes += str(points) + " "

        styleItem.setText(1, sizes.strip())

fontTree.show()

# Save to text file
with open("font_info.txt", "w") as f:
    for topLevelItemIndex in range(fontTree.topLevelItemCount()):
        topLevelItem = fontTree.topLevelItem(topLevelItemIndex)
        f.write(f"Font: {topLevelItem.text(0)}\n")
        for childIndex in range(topLevelItem.childCount()):
            childItem = topLevelItem.child(childIndex)
            f.write(f"  Style: {childItem.text(0)}\n")
            f.write(f"    Smooth Sizes: {childItem.text(1)}\n")
        f.write("\n")

app.exec_()
