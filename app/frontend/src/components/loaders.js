import { reuleaux, waveform } from "ldrs";
import { Fragment } from "react";
import Box from "@mui/material/Box";

waveform.register()
reuleaux.register()

export function ModalDataLoading() {
  return (
	<Fragment>
		<Box sx={{display: "flex", alignItems:"center", justifyContent:"center", width: "100%", height:"200px"}}>
			<l-reuleaux
				size="60"
				stroke="5"
				stroke-length="0.15"
				bg-opacity="0.1"
				speed="1.2"
				color="white"
				></l-reuleaux>
		</Box>
	</Fragment>
  );
}

export function PageLoading() {
  return (
	<Fragment>
		<Box sx={{display: "flex", alignItems:"center", justifyContent:"center", width: "100%", height:"60vh"}}>
			<l-waveform
				size="60"
				stroke="3.5"
				speed="1.2" 
				color="white" 
			></l-waveform>
		</Box>
	</Fragment>
  );
}