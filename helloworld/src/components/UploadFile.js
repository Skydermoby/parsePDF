import axios from "axios";
import React, { useState } from "react";
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});


const UploadFile = () => {
	const [selectedFile, setSelectedFile] = useState(null);
  const [savedData, setData] = useState(null);
  const [hasUpload, setUpload] = useState(false);
  const [canDownload, setDownload] = useState(true);
  const [canUpload, setCanUpload] = useState(true);
  const [message, setMessage] = useState("Please upload a pdf file to be converted into json")
	const onFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
		setDownload(true);
		setCanUpload(false);
		setMessage("Selected File: " + event.target.files[0].name);
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
	  setCanUpload(true)
	  setMessage("File successfully uploaded! Please wait for it to be converted")
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
    axios.get("http://127.0.0.1:8000/items/" + selectedFile.name)
    .then(res=>{
      console.log(JSON.parse(res.data))
      setData(res.data)
	  setMessage("File Conversion Completed! Please press the download button below!")
	  setDownload(false)
    })
    setUpload(false);
  }

	return (
		<div>
			<h1>Aaron's even shabbier front end 0_0</h1>
			<h3>PDF to JSON Conversion:</h3>
			<div>
				<Button
					component="label"
					role={undefined}
					variant="contained"
					tabIndex={-1}
					>
					Upload files
					<VisuallyHiddenInput
						type="file"
						onChange={onFileChange}
						multiple
					/>
				</Button>
				<Button onClick={onFileUpload} variant="contained" disabled={canUpload}>Upload!</Button>
			</div>
			<div>{message}</div>
			<Button onClick={onButtonClick} variant="contained" disabled={canDownload}> Download JSON File </Button>
		</div>
		
	);
};

export default UploadFile;