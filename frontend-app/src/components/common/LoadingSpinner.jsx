export default function LoadingSpinner() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-blue-50/80 to-indigo-100/80 backdrop-blur-md">
      <div className="relative flex flex-col items-center gap-4 p-6 bg-white/90 rounded-xl shadow-2xl">
        <div className="relative w-16 h-16">
          <div className="absolute inset-0 border-4 border-blue-200 rounded-full animate-pulse"></div>
          <div className="absolute inset-0 border-t-4 border-blue-600 rounded-full animate-spin"></div>
        </div>
        <div className="flex items-center gap-2">
          <p className="text-gray-800 text-base font-semibold tracking-tight animate-pulse">
            Memproses dokumen
          </p>
          <div className="flex gap-1"></div>
        </div>
      </div>
    </div>
  );
}