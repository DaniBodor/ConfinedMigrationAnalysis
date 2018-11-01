gridx = 5;	//number of images accross (x-dimension)
gridy = 3;	//number of images down (y-dimension)
channels = 3; //number of channels imaged //// CURRENTLY UNUSED, I BELIEVE
DriftCorrection = 0; // Use drift correction? ('Plugins>Registration>Correct 3D Drift')
StripFirstTP = 1; // Remove first time point?
ffblur = 15;	// Blurring factor for flat field correction. Set to 0 to turn off correction
COUNT=0;
overlap = 20; // % overlap

LUTList = 0;
// LUTlist sets correct conversion of channels to colors
// if 0 will read channels from metadata and apply LUTs accordingly:
// Violet = Cyan // Green = Green // Red/Yellow = Red // Far Red = Magenta
// Alternatively, set an array of LUTs using strings of correct LUTs
// LUTList = newArray("Magenta","Green","Grays");




//nameList=newArray("180809_2Dmig_CTYw+CTFR_6um_BSA");
//nameList=newArray("2Dmig_BSA_CFSE+CTFR_6um_002");
base=getDirectory("");

nameList=getFileList(base);


print("\\Clear");

for(i=0;i<nameList.length;i++){
	print (nameList[i]);
	runStitch(nameList[i]);
	print(":::");
}


print("gridx = "+gridx);
print("gridy = "+gridy);
print("DriftCorrection = "+DriftCorrection;)
print("StripFirstTP = "+StripFirstTP);
print("ffblur = "+ffblur);
print("overlap = "+overlap);

selectWindow("Log");
saveAs("Text", base+"macroLog.txt");





// ACTION FUNCTION
function runStitch(name) {

	/////
	/////	DEFINE IMAGE NAMES, ETC
	if (endsWith(name,".nd2"))	name = substring(name,0,lengthOf(name)-4);
	
	getDateAndTime(y,m,dW,dM,h,min,sec,msec);
	print("start time: "+h,":",IJ.pad(min,2),":",IJ.pad(sec,2));
	bigfile=base+name+".nd2";
	dir = base+name+File.separator;
	print(bigfile);

	/////
	/////	SKIP IF NOT IMAGE OR STARTS WITH UNDERSCORE
	if(File.exists(bigfile) && startsWith(name,"_")==0) {

		/////
		/////	CHECK IF FILE HAS PREVIOUSLY BEEN SPLIT
		if(File.isDirectory(dir)==0)	File.makeDirectory(dir);
		
		if(File.exists(dir+name+"_01.tif")){
			Dialog.create("");
				Dialog.addMessage("Individual position files potentially already exist");
				Dialog.addCheckbox("Ignore existing files and re-split .nd2-file now?",0);
//				Dialog.show();		// Uncomment this line in case I want the Dialog window to confirm this
			split_now=Dialog.getCheckbox();
		}else split_now=1;
		
		/////
		/////	SPLIT FILE INTO INDIVIDUAL POSITION FILES
		if(split_now==1){ // split large .nd2 file into individual position .tifs
			print(bigfile+" is now being opened");
			run("Bio-Formats", "open=" + bigfile + " autoscale color_mode=Default open_all_series rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
			getDateAndTime(y,m,dW,dM,h,min,sec,msec);
			print("files open: "+h,":",IJ.pad(min,2),":",IJ.pad(sec,2));
			
			Stack.getDimensions(width, height, channels, slices, frames);
			setSlice(nSlices());
			getStatistics(area, mean, min, max, std, histogram);
			metaD = getImageInfo();

			while (nImages>0){		
				selectImage(nImages);
				img=IJ.pad(nImages,2);   /// adds leading 0 for numbers under 10
				run("8-bit");
				run("Stack to Hyperstack...", "order=xyczt(default) channels="+channels+" slices=1 frames="+nSlices/channels+" display=Composite");
				LUTlist = FIX_BUGS(LUTlist);
				
				//// ?REMOVE FIRST TIMEPOINT? (OFTEN USED AT 20-40' INTERVAL TO SECOND TP)
				if (StripFirstTP == 1){
					setSlice(1);
					run("Delete Slice", "delete=frame");
				}
				
				saveAs("Tiff", dir+name+"_"+img+".tif");
				print("saved "+dir+name+"_"+img+".tif");
				close();
			}
		} else {
			//// THIS IS JUST TO LOAD THE METADATA TO SAVE INTO THE STITCHED IMAGE. 
			//// ONLY USED IN CASE OF PREVIOUSLY SPLIT FILES
			open(dir+name+"_01.tif");
			metaD = getImageInfo();
			close();
			print ("running macro on previously split files");
		}
	
		run("Close All");
		run("Collect Garbage");
		
		/////
		/////	STITCHING PART OF MACRO
		getDateAndTime(y,m,dW,dM,h,min,sec,msec);
		print("stitching files: "+dir+name+"_{ii}.tif");
		print("stitching start: "+h,":",IJ.pad(min,2),":",IJ.pad(sec,2));
		print("");
		run("Grid/Collection stitching", "type=[Grid: snake by rows] order=[Right & Down                ] grid_size_x="+gridx+" grid_size_y="+gridy+" tile_overlap="+overlap+" first_file_index_i=1 directory=["+dir+"] file_names=["+name+"_{ii}.tif] output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 subpixel_accuracy computation_parameters=[Save memory (but be slower)] image_output=[Fuse and display]");
		LUTlist = FIX_BUGS(LUTlist);
	
		/////
		/////	FLAT FIELD CORRECTIONS FIXES UNEQUAL ILLUMINATION BETWEEN FRAMES
		if (ffblur > 0){
			ABC=getTitle();
			run("Split Channels");
			for (f = 0; f < channels; f++) {
				Q = "C"+d2s(f+1,0)+"-"+ABC;	// system naming of images after file splitting
				selectImage(Q);
				run("Pseudo flat field correction", "blurring="+ffblur);
				selectImage(Q+"_background"); // system naming of bg image used for flat field correction
				close();
			}

// Loop below is probably replaced by last 2 lines in loop above. Needs to be tested
//			X=nImages;
//			for (f = 0; f < X; f++) {
//				selectImage(X-f);
//				AA = getTitle();
//				if (indexOf(AA,"background") > 0 )		close();
//			}
			
			run("Concatenate...", "all_open title="+ABC);
			run("Stack to Hyperstack...", "order=xytcz channels="+channels+" slices=1 frames="+nSlices/channels+" display=Composite");	
			LUTlist = FIX_BUGS(LUTlist);
		}
		setMetadata(metaD);
		saveAs("Tiff", dir+"Stitch_"+name+".tif");
		
		if (DriftCorrection == 1){
			run("Correct 3D drift", "channel=1 only=0 lowest=1 highest=1");
			saveAs("Tiff", dir+"Stitch_"+name+"_driftCorrected.tif");
		}
	
		//waitForUser("end of macro; from here will just close file and print final crap")
		run("Close All");
		run("Collect Garbage");
		
		getDateAndTime(y,m,dW,dM,h,min,sec,msec);
		print("finished: "+h,":",IJ.pad(min,2),":",IJ.pad(sec,2));
		print("");
	} else{
		print("skipping file");
	}
}


/////// SUBFUNCTION LIST

function FIX_BUGS(LUTlist){
	// fix frames  to slices conversion error
	Stack.getDimensions(width, height, channels, slices, frames);
	if (frames == 1)	
		Stack.getDimensions(width, height, channels, frames, slices);

	// apply correct LUTs and rescale
	if (LUTlist == 0)	LUTlist = FINDCHANNELS();	// reads channels from metadata
	for (x=0;x<channels;x++){
		Stack.setChannel(x+1);
		run(LUTlist[x]);
		getStatistics(area, mean, min, max, std, histogram);
		setMinAndMax(mean*1.5, max*0.5);
	}

	// delete last frame if empty
	setSlice(nSlices());
	getStatistics(area, mean, min, max, std, histogram);
	if  (max == 0)		run("Delete Slice", "delete=frame");

	setSlice(1);
	return LUTlist
}

function FINDCHANNELS() {

	// a lot of this overly complex code can be replaced with the "getInfo(key)" command!
	//print("\\Clear");
	Stack.getDimensions(width, height, channels, slices, frames)
	MD = getMetadata("");
	begindex = indexOf(MD,"Line:1; ExW:385; Power #1");
	endex = indexOf(MD,"LiveSpeedUp")+10;
	LineMD = substring(MD,begindex,endex);
	
	
//	begindex = indexOf(MD,"Modality");
//	endex = indexOf(MD,"Modified");
//	ModalMD = substring(MD,begindex,endex);
	
	
	begindex = indexOf(MD,"m_uiMultiLaserLineWavelength0-00");
	endex = indexOf(MD,"m_uiMultiLaserLines0");
	LLMD = substring(MD,begindex,endex);
	
	WL = newArray(4);
	for(n=0;n<4;n++){
		ix = indexOf(LLMD,"m_uiMultiLaserLineWavelength0-0"+d2s(n,0))+35;
		//print (ix);
		WL[n] = substring(LLMD,ix,ix+3);
		//print (WL[n]);
	}
	//exit("A");
	
	//WL = newArray(385,470,550,635);
	WL_order = newArray(channels);
	color = newArray(channels);
	
	
	
	for (n=0;n<4;n++){
		//print(n);
		WL_begindex = indexOf(LineMD,WL[n])-12;
		WL_endex = lastIndexOf(LineMD,WL[n])+30;
		LineN = substring(LineMD,WL_begindex,WL_endex);
		if (indexOf(LineN,"On") > 0){
			ChannelNumber = substring(LineN,0,indexOf(LineN,"On"));
			ChannelNumber = substring(ChannelNumber,lastIndexOf(ChannelNumber,"#")+1,lastIndexOf(ChannelNumber,"#")+2);
			WL_order[ChannelNumber-1] = WL[n];
			//print (WL[n],ChannelNumber);
		}
	}
	
	//print("---------");
	
	
	
	for (n=0;n<channels;n++){
		if		(WL_order[n]<100)	color[n] = "Grays";
		else if	(WL_order[n]<400)	color[n] = "Cyan";
		else if	(WL_order[n]<500)	color[n] = "Green";
		else if	(WL_order[n]<600)	color[n] = "Red";
		else 						color[n] = "Magenta";
	//	print (WL_order[n],color[n]);
	}
	return color;
}


function DELETE_BLANK_LAST_FRAME(){
	setSlice(nSlices());
	getStatistics(area, mean, min, max, std, histogram);
	if  (max == 0)		run("Delete Slice", "delete=frame");
}