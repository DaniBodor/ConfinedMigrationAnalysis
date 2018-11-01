FlatField = 1;
ffblur = 50;
Stack.getDimensions(width, height, channels, slices, frames);

	if (FlatField == 1){
		ABC=getTitle();
		run("Split Channels");
		for (f = 0; f < channels; f++) {
			selectImage("C"+d2s(f+1,0)+"-"+ABC);
			run("Pseudo flat field correction", "blurring="+ffblur);
		}
		
		X=nImages;
		for (f = 0; f < X; f++) {
			selectImage(X-f);
			AA = getTitle();
			if (indexOf(AA,"background") > 0 )		close();
		}
		
		run("Concatenate...", "all_open title="+ABC);
		run("Stack to Hyperstack...", "order=xytcz channels="+channels+" slices=1 frames="+nSlices/channels+" display=Composite");	
//		setMetadata(metaD);
		DELETE_EMPTY_FRAMES();

	}



function DELETE_EMPTY_FRAMES(){
	setSlice(nSlices());
	getStatistics(area, mean, min, max, std, histogram);
	if  (max == 0)		run("Delete Slice", "delete=frame");
}