LUT = "Ice"


print("\\Clear");

base = getDirectory("");
dir = base;

dirlist = getFileList(base);
list = getFileList(base);


for (j=0; j<dirlist.length;j++){	
	i=j;
//	if (endsWith(dirlist[j],File.separator)){
//		print (dirlist[j]);
//
//		list = getFileList(base+dirlist[j]);
//		for (i = 0; i < list.length; i++) {
//			dir = base+dirlist[j];
			if ( startsWith(list[i],"Stitch_")  && endsWith(list[i],".tif") ){
				open (dir+list[i]);
				run("Reduce Dimensionality...", "frames");

				//waitForUser("fsdgdfg");
				
				run("Temporal-Color Code", "lut=["+LUT+"] start=1 end="+nSlices);
				setMinAndMax(10, 40);
				saveAs("Tiff", base+list[i]+"_Temp-PRJ.tif");
				run("Close All");
			}
//		}
//	}
}

