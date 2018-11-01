//DuplicateRange = "31-210"

print ("\\Clear");
//run("Close All");

dir = getDirectory("");

out = dir+"TrackMate_Analysis"+File.separator;
File.makeDirectory(out);
firstline = "basedir='"+out+"'\n";

py = "TrackMate_JythonScript.py";
script = File.openAsString(dir+py);

script = firstline+script
//print (firstline)
//print (script);

//exit("");
list = newArray("2Ch_2tp_tester.tif")
//list = getFileList(dir);



for(i=0;i<list.length;i++){
	if (endsWith(list[i],".tif") && startsWith(list[i],"_")==0) {
		
		open(dir+list[i]);
		A=getTitle();

/*		run("Duplicate...", "duplicate range="+DuplicateRange);
		selectImage(A);
		close();
		A=getTitle();
*/

		Stack.getDimensions(width, height, channels, slices, frames);
		for (j=0;j<channels;j++){
			secondline= "TARGET_CHANNEL = "+d2s(j+1,0);
			print ("run python on:" , list[i] , "channel", d2s(j+1,0));
			eval("python",script);
			print ("python done:" , list[i] , "channel", d2s(j+1,0));
		}

		getPixelSize(unit, pixelWidth, pixelHeight);
		print("\nPixel size is " + pixelWidth + " x " + pixelHeight + " " + unit);

		selectWindow("Log");
		saveAs("Text", out+list[i]+"_Log.txt");
		wait(20*1000);
		run("Close");

		selectWindow("Spots in tracks statistics");
		saveAs("Results", out+list[i]+"_track_stats.csv");
		run("Close");

		selectWindow("Links in tracks statistics");
		run("Close");
		selectWindow("Track statistics");
		run("Close");

		run("Close All");
		run("Collect Garbage");
	}
}


// ALMOST THERE. FOR SOME REASON DATA IS NOT READABLE BY XY-EXTRACTOR SCRIPT.
// THIS COULD BE DUE TO ALLOWING MERGING/SPLITTING TRACKS --> correct
// TRY FIXING BY NOT ALLOWING THAT, OR REWRITE XY-EXTRACTOR (IT SHOULD WORK)
// FOR NOW WILL STICK TO NOT ALLOWING MERGE OR SPLIT EVENTS (SPLITTING WAS ALLOWED BEFORE)
