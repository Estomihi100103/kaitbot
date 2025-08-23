export default function Notification({ message, type = 'success', onClose }) {
  return (
    <div
      className={`${
        type === 'success' ? 'bg-green-100 border-green-400 text-green-700' : 'bg-red-100 border-red-400 text-red-700'
      } border px-4 py-2 rounded text-sm relative`}
    >
      {message}
      {onClose && (
        <button onClick={onClose} className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 cursor-pointer">
          X
        </button>
      )}
    </div>
  );
}