import React, { useState, useRef, useEffect } from "react";
// import ReactMarkdown from "react-markdown";
import Chat from "./component/Chat";
import Answer from "./component/Answer";
// import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
// import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function App() {
  const [answers, setAnswers] = useState([]); // store all answers
  const [isLoading, setIsLoading] = useState(false);
  const containerRef = useRef(null);

  const handleShowAnswer = (answer,questions) => {
    if (!answer) return;
    // setQuestion(questions.charAt(0).toUpperCase() + questions.slice(1)); // Capitalize first letter of question
    setAnswers((prev) => [...prev, "-------------------------\n\n--------------------------------", questions.charAt(0).toUpperCase() + questions.slice(1), answer]);
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
        <p className="text-lg font-semibold p-4">ForgeX</p>
        {/* <br/> */}
        <p className="text-lg font-thin mb-4">A smart AI research partner that turns complex information into clear, actionable knowledge.</p>
      </div>

      {/* Answer Display Area */}
      <div
        ref={containerRef}
        className={`${answers.length > 0 ? "justify-center h-fit w-[90%] mb-[15vh]  p-20 mx-auto mt-[5vh] text-lg text-gray-300  bg-gray-800 rounded-lg overflow-y-auto custom-scrollbar scroll-smooth" : ""}`}
      >

        {isLoading && (
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-xl text-white">
            Loading...
          </div>
        )}
         
        {/* Render each answer separately */}

        {answers.map((ans, idx) => (
          <Answer key={idx} content={ans} />
        ))}

      </div>

      {/* Chat Input Area */}
      <div className="flex bottom-2 w-[70%] p-2 gap-5 justify-center items-center mx-auto mt-5 bg-gray-800 rounded-lg">
        <div className="fixed w-[70%] bottom-2 left-1/2 transform -translate-x-1/2 bg-gray-700 rounded-lg p-2">
          <Chat viewAnswer={handleShowAnswer} setIsLoading={setIsLoading} />
        </div>
      </div>
    </>
  );
}

export default App;