import React, { useState, useRef, useEffect, useMemo } from "react";
// import ReactMarkdown from "react-markdown";
import Chat from "./component/ChatComponent";
import Answer from "./component/Answer";
// import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
// import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import loader from "./assets/loading.gif"
function App() {
  const [answers, setAnswers] = useState([]); // store all answers
  const [isLoading, setIsLoading] = useState(false);
  const containerRef = useRef(null);
  const MAX_ARRAY_LENGTH = 42949;

  const handleShowAnswer = (answer, questions, file) => {
    file = file !== null ? file : "";
    if (!answer) {
      console.log("no response found", answer);
      return;
    }
    console.log("Response : ", typeof answer, "-------------------\n\n");
    setAnswers((prev) => {
      if (prev.length >= MAX_ARRAY_LENGTH) {
        return ["Token exceeded ! Please try again "];
      }

      return [
        ...prev,
        "-------------------------\n\n--------------------------------",
        file + "\n\n",
        questions.charAt(0).toUpperCase() + questions.slice(1),
        answer
      ];
    });
  };

  // Auto-scroll when a new answer is added
  useEffect(() => {
    if (containerRef.current) {
      // containerRef.current.scrollIntoView({ behavior: "smooth", block: "end"});
    }
  }, [answers]);

  return (
    <>
      {/* Header */}
      <div className="fixed w-full h-auto z-10 top-0 text-center text-2xl font-semibold border-b border-gray-700 bg-gray-800 text-gray-300">
        <p className="text-lg font-semibold p-2 ">ForgeX <br/><span className="font-thin">A smart AI research partner</span></p>
      </div>

      {/* Answer Display Area */}
      <div
        ref={containerRef}
        className={`${answers.length > 0 ? "justify-center h-fit w-full md:w-[95%] lg:w-[80%]  mb-[40%]  p-8  mx-auto mt-[5vh] text-lg text-gray-300  bg-gray-800 rounded-lg overflow-y-auto custom-scrollbar scroll-smooth" : ""}`}
      >

        {isLoading && (
          <div className="fixed z-10 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-xl text-white">
            <img className="w-20 h-20 rounded-full bg-gray-800" src={loader} alt="Loading..."/>
          </div>
        )}

        {/* Render each answer separately */}

        {useMemo(()=>answers.map((ans, idx) => (
          <Answer key={idx} content={ans} />
        )))}

      </div>

      {/* Chat Input Area */}
      <div className="flex bottom-2 w-[90%] md:w-[95%] lg:w-[60%] sm:w-[100%] p-2 gap-5 justify-center items-center mx-auto mt-5 bg-gray-800 rounded-lg">
        <div className="fixed w-full md:w-[70%] lg:w-[60%] sm:w-[100%] bottom-2 left-1/2 transform -translate-x-1/2 bg-gray-700 rounded-lg p-2">
          <Chat viewAnswer={handleShowAnswer} setIsLoading={setIsLoading} />
        </div> 
      </div>
    </>
  );
}

export default App;