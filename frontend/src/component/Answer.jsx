import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

const ViewAnswer = React.memo(({ content = ""}) => {
  const safeContent = typeof content === "string" ? content : "";

  const CodeBlock = ({ inline, className, children, ...props }) => {
    const match = /language-(.+)/.exec(className || "");
    const [copied, setCopied] = useState(false);

    const codeString = String(children).replace(/\n$/, "");

    const handleCopy = async () => {
      await navigator.clipboard.writeText(codeString);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    };

    if (!inline) {
      return (
        <div className="relative my-4">
          {/* Copy Button */}
          <button
            onClick={handleCopy}
            className="absolute top-2 right-2 bg-gray-700 hover:bg-gray-600 text-xs px-2 py-1 rounded text-white transition"
          >
            {copied ? "Copied" : "Copy"}
          </button>

          <SyntaxHighlighter
            style={oneDark}
            language={match ? match[1] : "bash"}
            PreTag="div"
            customStyle={{
              
              borderRadius: "0.75rem",
              paddingTop: "2.5rem",
            }}
            {...props}
          >
            {codeString}
          </SyntaxHighlighter>
        </div>
      );
    }

    return (
      <code className="bg-gray-800 text-green-300 px-1 py-0.5 rounded text-xl">
        {children}
      </code>
    );
  };

  return (
    <>

    <div className="max-w-none text-gray-200 text-lg leading-relaxed">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code: CodeBlock,

          h1: ({ children }) => (
            <h1 className="text-3xl font-bold border-b border-gray-700 pb-2 my-4">
              {children}
            </h1>
          ),

          h2: ({ children }) => (
            <h2 className="text-2xl font-semibold border-b border-gray-700 pb-1 my-3">
              {children}
            </h2>
          ),

          h3: ({ children }) => (
            <h3 className="text-xl font-semibold my-2">
              {children}
            </h3>
          ),

          p: ({ children }) => (
            <p className="my-2 text-gray-300">{children}</p>
          ),

          ul: ({ children }) => (
            <ul className="list-disc pl-6 my-3 space-y-1">
              {children}
            </ul>
          ),

          ol: ({ children }) => (
            <ol className="list-decimal pl-6 my-3 space-y-1">
              {children}
            </ol>
          ),

          li: ({ children }) => (
            <li className="text-gray-300">{children}</li>
          ),

          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-400 my-4">
              {children}
            </blockquote>
          ),

          hr: () => (
            <hr className="border-gray-700 my-6" />
          ),

          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 underline hover:text-blue-300 transition"
            >
              {children}
            </a>
          ),

          /* ================= TABLE STYLING ================= */

          table: ({ children }) => (
            <div className="overflow-x-auto my-6 rounded-xl border border-gray-700">
              <table className="min-w-full text-sm text-left">
                {children}
              </table>
            </div>
          ),

          thead: ({ children }) => (
            <thead className="bg-gray-800 text-gray-200">
              {children}
            </thead>
          ),

          tbody: ({ children }) => (
            <tbody className="bg-gray-900 text-gray-300">
              {children}
            </tbody>
          ),

          tr: ({ children }) => (
            <tr className="border-b border-gray-700 hover:bg-gray-800 transition">
              {children}
            </tr>
          ),

          th: ({ children }) => (
            <th className="px-4 py-3 font-semibold border-r border-gray-700 last:border-none">
              {children}
            </th>
          ),

          td: ({ children }) => (
            <td className="px-4 py-3 border-r border-gray-800 last:border-none">
              {children}
            </td>
          ),
        }}
      >
        {safeContent}
      </ReactMarkdown>
    </div>
    </>
  );
});

export default ViewAnswer;