import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import '../custom.css';

function Chat({ viewAnswer, setIsLoading }) {

    const [question, setQuestion] = useState("");
    const [files, setFiles] = useState(null);
    // const [filetodislay, setFileToDisplay] = useState(null);
    const fileRef = useRef(null);

    const handleClick = () => {
        fileRef.current.click();
    }

    useEffect(() => {
        if (files) {
            console.log("Uploading file.....");


        }
    }, [files]);

    const handleUpload = async (event) => {
        const selectedFile = event.target.files[0];
        setFiles(selectedFile);


        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            setIsLoading(true);
            const response = await axios.post("/api/upload/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            const res = response.data;  // Axios already gives the parsed JSON
            setIsLoading(false);
            console.log("Final answer after uploading file : ", res);
            if (res.output && res.output.length > 0) {
                viewAnswer(res.output[0].text, questionToAsk);   // ✅ send to App component
            } else {
                viewAnswer("", questionToAsk);   // ✅ send empty answer to App component
            }

        } catch (error) {
            console.error("Error uploading file:", error);
            setIsLoading(false);
        }
    }

    const inputquestion = (e) => {
        setQuestion(e.target.value);
    }

    const askQuestion = async () => {
        const questionToAsk = question.trim();
        if (questionToAsk === "") return;

        setQuestion("");
        setFiles(null);

        try {
            setIsLoading(true);
            const res = await axios.post("/api/ask/", { question: questionToAsk });
            console.log("FULL RESPONSE:", res);
            console.log("RESPONSE DATA:", res.data);
            console.log("ANSWER FIELD:", res.data.answer);
            // setFiles(null);  // Clear the file state after upload
            viewAnswer(res.data.answer, questionToAsk);   // ✅ SEND ANSWER TO APP
            setIsLoading(false);
        } catch (error) {
            console.error("Something went wrong while asking the question:", error);
            setIsLoading(false);
        }
    }

    return (
        <>
            <div className={`${files?.name ? "flex justify-center items-center text-white text-xl mb-2 border-b-2" : ""}`}>{files?.name || ""}</div>

            <div className="flex flex-col w-full">

                <textarea
                    className="flex-1 h-auto w-full p-2 text-xl rounded-lg bg-gray-600 text-white focus:outline-none resize-none hide-scrollbar "
                    value={question}
                    onKeyDown={(e) => { if (e.key === "Enter" && question.trim() !== "") { askQuestion(); } }}
                    onChange={inputquestion}
                    rows={3}
                />

                <div className="flex items-center mt-2 justify-between w-full">
                    <div
                        className="cursor-pointer bg-gray-500 rounded-full w-10 h-10 flex items-center justify-center hover:bg-gray-400 text-lg"
                        onClick={handleClick}
                    >
                        +
                    </div>

                    <input
                        className="hidden"
                        ref={fileRef}
                        type="file"
                        onChange={handleUpload}
                    />

                    <button
                        className={`${question.trim() === "" && !files ? "text-white text-2xl font-bold bg-slate-800 w-10 h-10 mr-2 rounded-full " : "text-white cursor-pointer font-bold text-2xl bg-gray-500 w-10 h-10 mr-2 rounded-full"}`}
                        onClick={askQuestion}
                        disabled={question.trim() === ""}  // Disable if no question  
                    >
                        ↑
                    </button>
                </div>
            </div>
        </>
    )
}

export default Chat;