// src/App.jsx
import React, { useState } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import LectureForm from './components/LectureForm';
import LectureList from './components/LectureList';
import WeeklySchedule from './components/WeeklySchedule';
import ThemeToggle from './components/ThemeToggle';

function App() {
  // lecturesDict: { [lectureName: string]: Lecture[] }
  const [lecturesDict, setLecturesDict] = useState({});
  const [optimizedLectures, setOptimizedLectures] = useState([]);
  const [isScheduleOpen, setIsScheduleOpen] = useState(false);

  const addLecture = (newLecture) => {
    const { lectureName, day, startTime, endTime, lecturerName, roomNumber } = newLecture;
    setLecturesDict(prevDict => {
      const updatedDict = { ...prevDict };
      if (!updatedDict[lectureName]) {
        updatedDict[lectureName] = [];
      }

      updatedDict[lectureName].push({
        name: lectureName,
        day,
        startTime,
        endTime,
        lecturerName,
        roomNumber
      });
      return updatedDict;
    });

    toast.success('Lecture added successfully!');
  };

  const deleteLecture = (lectureName, targetLecture) => {
    setLecturesDict(prevDict => {
      const updatedDict = { ...prevDict };
      if (updatedDict[lectureName]) {
        updatedDict[lectureName] = updatedDict[lectureName].filter(
          lecture =>
            lecture.day !== targetLecture.day ||
            lecture.startTime !== targetLecture.startTime ||
            lecture.endTime !== targetLecture.endTime
        );
  
        if (updatedDict[lectureName].length === 0) {
          delete updatedDict[lectureName];
        }
      }
      return updatedDict;
    });
  };
  

  const showSchedule = () => {
    if (Object.keys(lecturesDict).length === 0) {
      toast.error('No lectures added!');
      return;
    }

    const schedule = calculateSchedules(lecturesDict);
    if (!schedule) {
      toast.error('No valid schedule found! Lectures are overlapping or no solution exists.');
      return;
    }
    setOptimizedLectures(schedule);
    setIsScheduleOpen(true);
  };

  // Helper functions ported from Python logic:
  const overlapCheck = (lec1, lec2) => {
    if (lec1.day !== lec2.day) return false;
    const lec1Start = timeToMinutes(lec1.startTime);
    const lec1End = timeToMinutes(lec1.endTime);
    const lec2Start = timeToMinutes(lec2.startTime);
    const lec2End = timeToMinutes(lec2.endTime);

    // Overlap if lec1End > lec2Start and both on same day
    return lec1Start < lec2End && lec2Start < lec1End;
  };

  const timeToMinutes = (t) => {
    const [hh, mm] = t.split(':').map(Number);
    return hh * 60 + mm;
  };

  const calculateSchedules = (lectureDict) => {
    // Convert dict to array of arrays
    const lectureGroups = Object.values(lectureDict).map(group => {
      // Sort each group by start time
      return [...group].sort((a, b) => timeToMinutes(a.startTime) - timeToMinutes(b.startTime));
    });

    const currentSchedule = [];
    return recursiveScheduling(lectureGroups, currentSchedule);
  };

  const recursiveScheduling = (lectureOptions, currentSchedule) => {
    // If no more options left, return currentSchedule
    if (!lectureOptions.some(opt => opt.length > 0)) {
      return [...currentSchedule];
    }

    const currentGroup = lectureOptions.shift();
    for (let lectureOption of currentGroup) {
      // Check if fits in currentSchedule without overlap
      if (!currentSchedule.some(scheduled => overlapCheck(lectureOption, scheduled))) {
        currentSchedule.push(lectureOption);
        const result = recursiveScheduling(lectureOptions, currentSchedule);
        if (result) {
          return result;
        }
        currentSchedule.pop();
      }
    }

    // Backtrack
    lectureOptions.unshift(currentGroup);
    return null;
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-200">
      <ThemeToggle />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-8">
          Lecture Management System
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-8">
            <LectureForm onAddLecture={addLecture} />
          </div>

          <div className="space-y-8">
            <LectureList lecturesDict={lecturesDict} onDeleteLecture={deleteLecture} />

            <button
              onClick={showSchedule}
              className="w-full px-4 py-2 text-white bg-primary-600 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-200"
            >
              Generate Schedule
            </button>
          </div>
        </div>

        <WeeklySchedule
          isOpen={isScheduleOpen}
          onClose={() => setIsScheduleOpen(false)} // Changed to onClose
          lectures={optimizedLectures}
        />
      </div>

      <Toaster position="top-right" />
    </div>
  );
}

export default App;
