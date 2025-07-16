import axios from "axios";
import React, { useState } from "react";

const PineconeQuarry = () => {
	const [quarryText, setQuarryText] = useState(null);
  	const [message, setMessage] = useState("ENter the text you would like to use for your semantic quarry")
	const onTextChange = (event) => {
		setQuarryText(event.target.value);
	};
	const onTextUpload = () => {
		console.log(quarryText);
		axios.get("http://127.0.0.1:8000/pinecone/" + quarryText.name)
    .then(res => {
      console.log(res)
	  setMessage(JSON.stringify(res.data))
    })
	};

	return (
		<div>
			<h3>Pinecond Database Quarry</h3>
			<div>
				<input type="text" onChange={onTextChange} /> 
				<button onClick={onTextUpload}>Quarry!</button>
			</div>
			<div>{message}</div>
		</div>
		
	);
};

export default PineconeQuarry;