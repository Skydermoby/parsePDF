import axios from "axios";
import React, { useState } from "react";

const PineconeWork = () => {
	const [selectedFile, setSelectedFile] = useState(null);
  	const [savedData, setData] = useState(null);
  	const [hasUpload, setUpload] = useState(false);
  	const [message, setMessage] = useState("Please upload a pdf file to upload to vector data base")
	const onFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
	};
	const onFileUpload = () => {
		const formData = new FormData();
		formData.append(
			'file',
			selectedFile,
			selectedFile.name
		);
		console.log(selectedFile);
		axios.post("http://127.0.0.1:8000/uploadfile/", formData, {headers: {'Content-Type': 'multipart/form-data'}})
    .then(res => {
      console.log(res)
      setUpload(true)
	  setMessage("File successfully uploaded! Please wait for it to be processed")
    })
	};
	const fileData = () => {
		if (savedData) {
      return (
        <div>
          <h2>File Conversion Completed! Please press the download button below!</h2>
        </div>
      );
    }
    else if (hasUpload) {
      <div>
          <h2>File successfully uploaded! Please wait for it to be converted</h2>
        </div>
    }
    else if (!hasUpload) {

    }
    else if (selectedFile) {
			return (
				<div>
					<h2>File Details:</h2>
					<p>File Name: {selectedFile.name}</p>
					<p>File Type: {selectedFile.type}</p>
					<p>
						Last Modified: {selectedFile.lastModifiedDate.toDateString()}
					</p>
				</div>
			);
		} 
    else {
			return (
				<div>
					<br />
					<h4>Choose before Pressing the Upload button</h4>
				</div>
			);
		}
	};

  const onButtonClick = () => {
    if (savedData) {
      const link = document.createElement("a");
      link.href = 'data:' + 'application/json;charset=utf-8;' + ',' + encodeURIComponent((savedData));
      let tempName = selectedFile.name
      const nmArray = tempName.split(".")
      link.download = nmArray[0]+".json";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }

  if (hasUpload) {
    axios.get("http://127.0.0.1:8000/pineconeUplpoad/" + selectedFile.name)
    .then(res=>{
      console.log((res.data))
      setData(res.data)
	  setMessage(JSON.stringify(res.data))
    })
    setUpload(false);
  }

	return (
		<div>
			<h3>Pinecond Database Upload</h3>
			<div>
				<input type="file" onChange={onFileChange} /> 
				<button onClick={onFileUpload}>Upload!</button>
			</div>
			<div>{message}</div>
		</div>
		
	);
};

export default PineconeWork;