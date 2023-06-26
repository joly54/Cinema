import React from "react";

const LoadingBar = () => (
    <div
        style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        }}
    >
        <svg
            style={{
                animation: "spin 2s linear infinite",
                marginLeft: "-1px",
                marginRight: "3px",
                height: "1rem",
                width: "1rem",
                color: "white"
            }}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
        >
            <circle
                style={{ opacity: "0.25" }}
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
            />
            <path
                style={{ opacity: "0.75", fill: "currentColor" }}
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.94l3-2.65z"
            />
        </svg>
        <style>
            {`
      @keyframes spin {
        0% {
          transform: rotate(0deg);
        }
        100% {
          transform: rotate(360deg);
        }
      }
      `}
        </style>
    </div>
);

export default LoadingBar;