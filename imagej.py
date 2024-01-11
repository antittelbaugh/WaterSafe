import imagej
import scyjava as sj
import matplotlib.pyplot as plt
#import jnius
#import numpy as np

# Initialize ImageJ
ij = imagej.init(mode='interactive')
print(f"ImageJ version: {ij.getVersion()}")
Overlay = sj.jimport('ij.gui.Overlay')
Table = sj.jimport('org.scijava.table.Table')
ParticleAnalyzer = sj.jimport('ij.plugin.filter.ParticleAnalyzer')
#Analyzer = sj.jimport('ij.plugin.filter.Analyzer')
imp1 = ij.io().open("/home/ashley/Imagej_testing/MPP_Images/Calcium_1.tif")
imp = ij.py.to_imageplus(imp1)
ij.ui().show(imp)
ij.IJ.setAutoThreshold(imp,"Default dark")
ij.IJ.setRawThreshold(imp, 15000,65535 )
ij.IJ.run(imp,"Set Scale...", "distance=20 known=10 unit=um")
ij.IJ.run("Set Measurements..."," feret's")
rt = ij.ResultsTable.getResultsTable()
ParticleAnalyzer.setResultsTable(rt)
ij.IJ.run("Analyze Particles...", "size=10-Infinity clear show=Overlay summarize=True", imp=imp)
sci_table = ij.convert().convert(rt,Table)
df=ij.py.from_java(sci_table)
df = df[(df['Feret'])> 40]
plt.hist(df['Feret'],bins='auto', alpha=.7, rwidth=.85)
plt.title('Microplastic Size Distribution')
plt.xlabel('Size(um)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--',alpha=.7)
plt.show()
print(f"Concentration: {len(df)} particles/L")
