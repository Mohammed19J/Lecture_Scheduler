// src/components/WeeklySchedule.jsx
import React, { useEffect, useState, useRef } from 'react';
import ReactDOM from 'react-dom';

// Define the days and time slots
const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const START_HOUR = 8;
const END_HOUR = 20;
const SLOT_DURATION = 30; // in minutes

// Generate time slots
const generateTimeSlots = () => {
  const slots = [];
  for (let hour = START_HOUR; hour < END_HOUR; hour++) {
    slots.push(`${String(hour).padStart(2, '0')}:00`);
    slots.push(`${String(hour).padStart(2, '0')}:30`);
  }
  slots.push(`${END_HOUR}:00`);
  return slots;
};

const TIME_SLOTS = generateTimeSlots();

// Utility functions
const timeToMinutes = (time) => {
  const [hour, minute] = time.split(':').map(Number);
  return hour * 60 + minute;
};

const getSlotIndex = (time) => {
  const startMins = timeToMinutes(`${START_HOUR}:00`);
  const currentMins = timeToMinutes(time);
  return Math.max(0, Math.floor((currentMins - startMins) / SLOT_DURATION));
};

const generateColor = () => {
  const hue = Math.floor(Math.random() * 360);
  const saturation = 60 + Math.floor(Math.random() * 20);
  const lightness = 70 + Math.floor(Math.random() * 10);
  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
};

// Accessibility hook to trap focus within the modal
function useFocusTrap(isOpen, modalRef) {
  useEffect(() => {
    if (!isOpen || !modalRef.current) return;

    const focusableElements = modalRef.current.querySelectorAll(
      'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleKeyDown = (e) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    modalRef.current.addEventListener('keydown', handleKeyDown);
    firstElement?.focus();

    return () => {
      if (modalRef.current) {
        modalRef.current.removeEventListener('keydown', handleKeyDown);
      }
    };
  }, [isOpen, modalRef]);
}

export default function WeeklySchedule({ isOpen, onClose, lectures = [] }) {
  const [lectureColors, setLectureColors] = useState({});
  const modalRef = useRef(null);

  // Assign colors to lectures
  useEffect(() => {
    const colors = {};
    lectures.forEach((lec) => {
      if (!colors[lec.name]) {
        colors[lec.name] = generateColor();
      }
    });
    setLectureColors(colors);
  }, [lectures]);

  // Organize lectures by day and slot
  const schedule = {};
  DAYS.forEach((day) => {
    schedule[day] = {};
  });

  lectures.forEach((lecture) => {
    const day = DAYS.find(
      (d) => d.toLowerCase() === lecture.day.toLowerCase()
    );
    if (!day) {
      console.warn(`Invalid day "${lecture.day}" for lecture "${lecture.name}"`);
      return;
    }

    const startIdx = getSlotIndex(lecture.startTime);
    const endIdx = getSlotIndex(lecture.endTime);
    const span = endIdx - startIdx || 1;

    // Prevent overlapping lectures
    if (schedule[day][startIdx]) {
      console.warn(`Overlapping lecture at ${lecture.startTime} on ${day}`);
      return;
    }

    schedule[day][startIdx] = { lecture, span };
  });

  // Trap focus within modal when open
  useFocusTrap(isOpen, modalRef);

  // Handle Escape key to close modal
  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === 'Escape') {
        console.log('Escape key pressed');
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
    }

    return () => {
      document.removeEventListener('keydown', handleEsc);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div
      className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      aria-modal="true"
      role="dialog"
      aria-labelledby="weekly-schedule-title"
      onClick={onClose} // Click outside to close
    >
      <div
        ref={modalRef}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-lg w-11/12 max-w-5xl max-h-[90vh] overflow-y-auto p-6 relative"
        onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
      >
        <h2
          id="weekly-schedule-title"
          className="text-2xl font-semibold text-gray-800 dark:text-white mb-4"
        >
          Weekly Schedule
        </h2>
        <button
          onClick={() => {
            console.log('Close button clicked');
            onClose();
          }}
          className="absolute top-4 right-4 text-gray-500 dark:text-gray-300 hover:text-gray-700  dark:hover:text-white focus:outline-none text-2xl"
          aria-label="Close modal"
        >
          &times;
        </button>
        <div className="overflow-x-auto">
          <table className="min-w-full table-auto border-collapse">
            <thead>
              <tr>
                <th className="sticky top-0 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 p-2 text-left text-sm font-medium text-gray-800 dark:text-white w-24">
                  Time
                </th>
                {DAYS.map((day) => (
                  <th
                    key={day}
                    className="sticky top-0 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 p-2 text-center text-sm font-medium text-gray-800 dark:text-white w-40"
                  >
                    {day}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {TIME_SLOTS.map((time, rowIndex) => (
                <tr key={time}>
                  <td className="border border-gray-200 dark:border-gray-700 p-2 text-sm text-gray-700 dark:text-gray-200">
                    {time}
                  </td>
                  {DAYS.map((day) => {
                    const cell = schedule[day][rowIndex];
                    if (cell) {
                      const { lecture, span } = cell;
                      const bgColor = lectureColors[lecture.name] || '#ccc';
                      const hslMatch = bgColor.match(/hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)/);
                      const lightness = hslMatch ? parseInt(hslMatch[3], 10) : 50;
                      const textColor = lightness > 50 ? 'text-gray-800' : 'text-white';
                      return (
                        <td
                          key={`${day}-${rowIndex}`}
                          rowSpan={span}
                          className={`border border-gray-200 dark:border-gray-700 p-2 ${textColor}`}
                          style={{ backgroundColor: bgColor }}
                        >
                          <div className="flex flex-col h-full">
                            <span className="font-medium">{lecture.name}</span>
                            <span className="text-xs">Lecturer: {lecture.lecturerName}</span>
                            <span className="text-xs">Room: {lecture.roomNumber}</span>
                            <span className="mt-auto text-xs">
                              {lecture.startTime} - {lecture.endTime}
                            </span>
                          </div>
                        </td>
                      );
                    }
                    // Check if the current cell is covered by a rowspan
                    for (let i = 1; i <= 24; i++) {
                      if (
                        schedule[day][rowIndex - i] &&
                        schedule[day][rowIndex - i].span > i
                      ) {
                        return null;
                      }
                    }
                    // Empty cell for no lecture
                    return (
                      <td key={`${day}-${rowIndex}`} className="border border-gray-200 dark:border-gray-700 p-2"></td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>,
    document.body
  );
}
