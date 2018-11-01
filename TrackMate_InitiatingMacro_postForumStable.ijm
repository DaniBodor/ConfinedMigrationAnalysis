
dir = getDirectory("");
list = getFileList(dir);
//list = newArray("000_Small_Tester.tif")

out = dir+"TrackMate_Analysis"+File.separator;
File.makeDirectory(out);
basedir_line = "basedir='"+out+"'\n";	// this line will be added to python script to generate the variable from this macro

py = "TrackMate_JythonScript_SparseLAP.py";
script = File.openAsString(dir+py);
//print (script);		exit("");


print ("\\Clear");
run("Close All");
run("Collect Garbage");
statsWindows = newArray("Spots in tracks statistics","Track statistics","Links in tracks statistics");
for (i = 0; i < 3; i++) {
	if(isOpen(statsWindows[i])){
		selectWindow(statsWindows[i]);
		run("Close");
	}
}


WindowName_short = "Memory_tracker";
if (!isOpen(WindowName_short))	run("New... ", "name="+WindowName_short+" type=Table");
WindowName = "["+WindowName_short+"]";
print(WindowName,"macro start:  "+IJ.freeMemory()+"\n");

//waitForUser("reposition Memory_tracker and Log windows");

for(i=0;i<list.length;i++){
	print(list[i]);
	if (endsWith(list[i],".tif") && !startsWith(list[i],"_")) {
//		print(dir+list[i]);}} exit("comment out this line containing an exit call (line 36?)");

		print("\\Clear");
		PRINT_TIME("opening file: "+list[i]);
		open(dir+list[i]);
		A=getTitle();
		Stack.getDimensions(width, height, channels, slices, frames);
//		print("don't forget to uncomment print-clear in line ~48");
		for (j=1;j<channels+1;j++){
			Modality = getInfo("Modality #"+j);
			data = list[i] + " --- Channel " + j;
			
			if (Modality != "Widefield Fluorescence")	// note the unequality symbol here
				print ("not running python on widefield:",data,"\n");
			else{
				Stack.setChannel(j);
				Stack.setDisplayMode("grayscale");
				before=getTime();
				
				PRINT_TIME ("run python on: " + data);
				print("\n");
				// the next 2 lines will be called with the python script to generate the variable from this macro
				channel_line = "TARGET_CHANNEL = " + j + "\n";	
				savename_line = "savename = r'"+out+data+"_TrackMate.xml'\n";		//raw string passed (I hope)
				eval("python",channel_line + savename_line + script);
				
				after=getTime();
				duration = round((after-before)/1000);
				PRINT_TIME ("Trackmate finished ("+duration+" s)");

				//save track and spots statistics
				selectWindow("Spots in tracks statistics");
				nSpots = getValue("results.count");
				saveAs("Results", out+data+"_SpotsStats.csv");
				run("Close");
				selectWindow("Track statistics");
				nTracks = getValue("results.count");
				//saveAs("Results", out+data+"TrackStats.csv");		//for some reason this window comes out empty...
				run("Close");
				selectWindow("Links in tracks statistics");
				nLinks = getValue("results.count");
				run("Close");
				print("Spots:",nSpots,"\nTracks:",nTracks,"\nLinks:",nLinks);
				
				/// the following lines are printing to the memory tracker
				print(WindowName,"#########\n#########\n");
				print(WindowName,data+"\n");
				print(WindowName,"Filesize: "+"\n");
				print(WindowName,"pre garbage collection:  "+IJ.freeMemory()+"\n");
				run("Collect Garbage");
				print(WindowName,"post garbage collection: "+IJ.freeMemory()+"\n");
			}
			print("---------------");
		}
		getPixelSize(unit, pixelWidth, pixelHeight);
		print("\nPixel size is (" + pixelWidth + "x" + pixelHeight + ") " + unit);	
		
		selectWindow("Log");
		saveAs("Text", out+list[i]+"_Log.txt");
		close();

		/// the following lines are printing to the memory tracker
		print(WindowName,"#########\n#########\n");
		for(XYX=0;XYX<10;XYX++){
			run("Collect Garbage");
			print(WindowName,"garbage collector " + (XYX+1) + ": " +IJ.freeMemory() +"\n");
		}
	}
}

selectWindow(WindowName_short);
saveAs("Text", out+WindowName_short + d2s(getTime(),0) + ".txt");

PRINT_TIME("");
print("\n############\nMACRO IS FINISHED!\n############\n");



// ALMOST THERE. FOR SOME REASON DATA IS NOT READABLE BY XY-EXTRACTOR SCRIPT.
// THIS COULD BE DUE TO ALLOWING MERGING/SPLITTING TRACKS --> correct
// TRY FIXING BY NOT ALLOWING THAT, OR REWRITE XY-EXTRACTOR (IT SHOULD WORK)
// FOR NOW WILL STICK TO NOT ALLOWING MERGE OR SPLIT EVENTS (SPLITTING WAS ALLOWED BEFORE)

// TRACK SPLITTING SEEMS TO BE OK NOW. ALTHOUGH THAT MIGHT BE BECAUSE THERE WAS NO SPLITTING EVENTS AT THIS POINT...



function PRINT_TIME(string){
	getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
	current_date = "" + year-2000 + IJ.pad(month+1,2) + IJ.pad(dayOfMonth,2);
	
	hour = IJ.pad(hour,2);
	min = IJ.pad(minute,2);
	sec = IJ.pad(second,2);
	curr_time = hour+":"+min+":"+sec;
	print(current_date,curr_time,"-",string);
}
