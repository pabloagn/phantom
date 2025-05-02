// packages/phantomklange/src/app/contributors/page.tsx
// @ts-nocheck

export const metadata = {
  title: 'Contributors | PhantomKlange',
  description: 'Meet the scholars, editors, and contributors to the PhantomKlange digital canon'
};

export default function ContributorsPage() {
  return (
    <div className="py-12 max-w-screen-lg mx-auto px-4">
      <h1 className="text-4xl font-bold">Contributors</h1>
      <p className="mt-4 mb-8">
        Meet the scholars, editors, and contributors who help build and maintain the PhantomKlange digital canon.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="flex flex-col items-center p-6 border rounded-lg text-center">
          <div className="w-24 h-24 bg-gray-300 rounded-full mb-4"></div>
          <h3 className="text-xl font-semibold">Dr. Elizabeth Chen</h3>
          <p className="text-sm text-gray-600 mt-1">Literary Historian, Yale University</p>
          <p className="mt-3">
            Specializes in comparative literature with a focus on East Asian and European literary traditions.
          </p>
        </div>

        <div className="flex flex-col items-center p-6 border rounded-lg text-center">
          <div className="w-24 h-24 bg-gray-300 rounded-full mb-4"></div>
          <h3 className="text-xl font-semibold">Prof. James Wilson</h3>
          <p className="text-sm text-gray-600 mt-1">Digital Humanities Lead, Oxford University</p>
          <p className="mt-3">
            Explores the intersection of technology and humanities in preserving and studying cultural artifacts.
          </p>
        </div>
      </div>
    </div>
  );
}
