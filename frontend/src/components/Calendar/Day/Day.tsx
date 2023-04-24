import React from 'react';
import { Grid } from '@mui/material';
import i18n from 'i18next';
import { EventProps } from '../../../Props/Event';
import { EventBlock } from './EventBlock/EventBlock';
import { TimeBlock } from './TimeBlock/TimeBlock';
import './Day.scss';

/**
 * Sort events according to their position.
 * @param eventKeyList The index of events to sort.
 * @param events The global list of events.
 * @returns The list of events sorted.
 */
export function sortWithPos(
  eventKeyList: Array<number>,
  events: Array<EventProps>
): Array<number> {
  const eventChain = [];
  let currentSize = 0;
  let currentEvent = 0;
  let hasBlanked = false;
  let blankUsed = false;
  let blankedEventKey: number;
  const { globalSize } = events[eventKeyList[0]];

  while (
    currentSize !== globalSize &&
    (currentEvent < eventKeyList.length || hasBlanked)
  ) {
    if (currentEvent < eventKeyList.length) {
      // If a blanked event exist, set hasBlanked to true and get the key (= size) of the blanked event
      if (eventKeyList[currentEvent] < 0 && !blankUsed) {
        hasBlanked = true;
        blankedEventKey = currentEvent;
        currentEvent += 1;
      } else if (
        eventKeyList[currentEvent] >= 0 &&
        events[eventKeyList[currentEvent]].position === currentSize
      ) {
        eventChain.push(eventKeyList[currentEvent]);
        currentSize += events[eventKeyList[currentEvent]].effectiveSize;
        currentEvent = 0;
      } else {
        currentEvent += 1;
      }
    } else {
      // Use the blanked event if it's necessary
      eventChain.push(eventKeyList[blankedEventKey]);
      currentSize -= eventKeyList[blankedEventKey];
      currentEvent = 0;
      hasBlanked = false;
      blankUsed = true;
    }
  }
  if (currentSize !== globalSize) {
    throw new Error(`Event chain is wrong`);
  }
  return eventChain;
}

/**
 * The Day component which contains all the TimeBlocks and EventBlocks of this day.
 * @param day The date of the events.
 * @param events The list of events in corresponding day.
 * @param chains The list of blocked chains.
 * @returns The Day component.
 */
export function Day(props: {
  day: Date;
  events: Array<EventProps>;
  chains: Array<Array<number>>;
}): JSX.Element {
  const { day, events, chains } = props;
  const hourBlockChain = [];
  for (let hour = 0; hour < 24; hour++) {
    hourBlockChain.push(<TimeBlock key={hour} startTime={hour}></TimeBlock>);
  }

  // Sort Event chains
  for (let i = 0; i < chains.length; i++) {
    chains[i] = sortWithPos(chains[i], events);
  }

  // Check whether events are already placed
  const toPlace = [];
  for (let i = 0; i < events.length; i++) {
    toPlace.push(i);
  }

  const eventsBeginTime = [];

  events.forEach((event) => {
    let startTime = 24;
    if (
      event.startDate.getDate() === day.getDate() &&
      event.startDate.getMonth() === day.getMonth() &&
      event.startDate.getFullYear() === day.getFullYear()
    ) {
      if (
        event.startDate.getHours() !== 0 ||
        event.startDate.getMinutes() !== 0 ||
        event.startDate.getSeconds() !== 0
      ) {
        startTime =
          23 -
          event.startDate.getHours() +
          (59 - event.startDate.getMinutes()) / 60 +
          (60 - event.startDate.getSeconds()) / 3600;
      }
    }
    eventsBeginTime.push(startTime);
  });

  return (
    <div
      id={`${day.toLocaleDateString('en-EN', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
      })}`}
      className="blockDisplay"
    >
      <div className="dayData">
        {day.toLocaleDateString(i18n.language, { weekday: 'narrow' })}
      </div>
      <div className="dayData">{day.getDate()}</div>
      {hourBlockChain}
      {chains.map((chain) => (
        <Grid
          container
          key={`Chain${chain}Day${day.toLocaleDateString('en-EN', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
          })}`}
          data-testid={`GlobalDayContainer${day.toLocaleDateString('en-EN', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
          })}TestId`}
        >
          {chain.map((eventKey) => {
            if (eventKey >= 0) {
              // If the event is not already displayed
              if (toPlace.includes(eventKey)) {
                toPlace.splice(toPlace.indexOf(eventKey), 1);
                return (
                  <Grid
                    item
                    key={events[eventKey].slug}
                    xs={
                      (events[eventKey].effectiveSize * 12) /
                      events[eventKey].globalSize
                    }
                    sx={{
                      height: `0px`,
                      transform: `translate(0px, -${
                        1.2 * eventsBeginTime[eventKey]
                      }rem)`,
                    }}
                  >
                    <EventBlock
                      key={events[eventKey].slug}
                      day={day}
                      event={events[eventKey]}
                    />
                  </Grid>
                );
              }

              // If the event has already been displayed
              return (
                <Grid
                  item
                  key={events[eventKey].slug}
                  xs={
                    (events[eventKey].effectiveSize * 12) /
                    events[eventKey].globalSize
                  }
                  sx={{
                    height: `0px`,
                    transform: `translate(0px, -${
                      1.2 * eventsBeginTime[eventKey]
                    }rem)`,
                  }}
                ></Grid>
              );
            }

            // return a blanked Event
            return (
              <Grid
                item
                key={eventKey}
                xs={(-eventKey * 12) / events[0].globalSize}
                sx={{
                  height: `0px`,
                }}
              ></Grid>
            );
          })}
        </Grid>
      ))}
    </div>
  );
}
