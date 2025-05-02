// packages/phantomklange/src/app/contributors/[slug]/loading.tsx

export default function Loading() {
  return (
    <div className="py-12 max-w-screen-lg mx-auto px-4">
      <div className="animate-pulse">
        <div className="h-10 bg-gray-200 rounded w-1/3 mb-6"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3 mb-8"></div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="border rounded-lg overflow-hidden">
              <div className="aspect-[3/2] bg-gray-200"></div>
              <div className="p-4">
                <div className="h-5 bg-gray-200 rounded w-2/3 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2 mb-3"></div>
                <div className="flex justify-between">
                  <div className="h-3 bg-gray-200 rounded w-10"></div>
                  <div className="h-3 bg-gray-200 rounded w-14"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
