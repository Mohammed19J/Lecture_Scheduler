import React from 'react';
import { TrashIcon } from '@heroicons/react/24/outline';

export default function LectureList({ lecturesDict, onDeleteLecture }) {
  // Flatten the dictionary to display all lectures
  // We'll display them grouped by lecture name
  const entries = Object.entries(lecturesDict);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <div className="p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Lecture List</h2>
        <div className="space-y-4">
          {entries.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 text-center py-4">
              No lectures added yet
            </p>
          ) : (
            entries.map(([lectureName, lectures]) => (
              lectures.map((lecture, index) => (
                <div
                  key={lectureName + index}
                  className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors duration-200"
                >
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {lecture.name}
                    </h3>
                    <div className="mt-1 text-sm text-gray-600 dark:text-gray-300">
                      <p>Lecturer: {lecture.lecturerName}</p>
                      <p>Room: {lecture.roomNumber}</p>
                      <p>
                        {lecture.day} • {lecture.startTime} - {lecture.endTime}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => onDeleteLecture(lectureName, lecture)} // Pass lecture object here
                    className="ml-4 p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 rounded-full hover:bg-red-100 dark:hover:bg-red-900 transition-colors duration-200"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              ))
            ))
          )}
        </div>
      </div>
    </div>
  );
}
