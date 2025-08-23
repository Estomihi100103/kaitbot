import { useState } from 'react';

export default function EmbedCode({ companySlug }) {
  const [showEmbedCode, setShowEmbedCode] = useState(false);

  const getEmbedCode = () => {
    return `<script src="http://localhost:8000/api/v1/chatbot/embed/${companySlug}.js" defer></script>`;
  };

  return (
    <div>
      <div className="flex justify-end">
        <button
          onClick={() => setShowEmbedCode(!showEmbedCode)}
          className="inline-flex px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200 cursor-pointer"
        >
          {showEmbedCode ? 'Sembunyikan Embed Code' : 'Tampilkan Embed Code'}
        </button>
      </div>
      {showEmbedCode && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg shadow-sm">
          <pre className="text-sm font-mono text-gray-800 bg-white p-3 rounded-md">{getEmbedCode()}</pre>
          <button
            onClick={() => {
              navigator.clipboard.writeText(getEmbedCode());
              alert('Embed code copied!');
            }}
            className="mt-3 px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-md hover:bg-indigo-700 transition duration-200 cursor-pointer"
          >
            Copy Code
          </button>
        </div>
      )}
    </div>
  );
}





// export default function EmbedCode({ companySlug }) {

//   const getEmbedCode = () => {
//     return `<script src="http://localhost:8000/api/v1/chatbot/embed/${companySlug}.js" defer></script>`;
//   };

//   return (
//     <div className="mb-4">
//       <div className="p-4 bg-gray-200 rounded-lg shadow-sm">
//         <pre className="text-sm font-mono text-gray-800 bg-gray-50 p-3 rounded-md">{getEmbedCode()}</pre>
//         <button
//           onClick={() => {
//             navigator.clipboard.writeText(getEmbedCode());
//             alert('Embed code copied!');
//           }}
//           className="mt-4 p-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition duration-200"
//         >
//           Copy Code
//         </button>
//       </div>
//     </div>
//   );
// }