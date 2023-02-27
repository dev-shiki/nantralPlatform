import {
  Button,
  Card,
  Grid,
  Skeleton,
  SvgIcon,
  Typography,
} from '@mui/material';

import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { EventProps } from 'Props/Event';
import { ClubProps } from 'Props/Club';
import React from 'react';
import { NavLink } from 'react-router-dom';
import ClubAvatar from '../../components/ClubAvatar/ClubAvatar';
import EventCard from '../../components/EventCard/EventCard';
import { ReactComponent as NantralIcon } from '../../assets/logo/scalable/logo.svg';
import './Home.scss';

const maxEventCount = 6;
const clubAvatarSize = 120;
/**
 * Home Page, with Welcome message, next events, etc...
 * @returns Home page component
 */
function Home(props) {
  const [events, setEvents] = React.useState<Array<EventProps>>(undefined);
  const [myClubs, setMyClubs] = React.useState<Array<ClubProps>>(undefined);
  const { t } = useTranslation('translation'); // translation module
  const headerImageURL =
    'https://www.ec-nantes.fr/medias/photo/carroussel-campus-drone-002_1524738012430-jpg';
  React.useEffect(() => {
    getEvent();
    getMyClubs();
  }, []);

  async function getEvent() {
    axios
      .get('api/event')
      .then((res) => {
        setEvents(res.data);
      })
      .catch((err) => console.error(err));
  }
  async function getMyClubs() {
    axios
      .get('api/club/my-clubs')
      .then((res) => {
        setMyClubs(res.data);
      })
      .catch((err) => console.error(err));
  }

  const LoadingSkeleton = (
    <>
      {[0, 1, 2].map((item, key) => (
        <Skeleton
          variant="rectangular"
          width={Math.min(
            (Math.max(
              document.documentElement.clientWidth,
              window.innerWidth || 0
            ) *
              2) /
              3,
            450
          )}
          height={Math.min(
            Math.max(
              document.documentElement.clientWidth,
              window.innerWidth || 0
            ) / 2,
            300
          )}
          key={item}
          style={{ margin: 10, borderRadius: 10 }}
        />
      ))}
    </>
  );

  const myEvents = (
    <Card variant="outlined" className="card">
      <SectionTitle title={t('home.myEvents')} url="/event" />
      <Grid spacing={0} container className="upcoming-event">
        {events
          ? events
              .slice(0, 3)
              .map((event) => <EventCard event={event} key={event.slug} />)
          : LoadingSkeleton}
      </Grid>
    </Card>
  );

  const upcomingEvents = (
    <Card variant="outlined" className="card">
      <SectionTitle title={t('home.upcomingEvents')} url="/event" />
      <Grid spacing={0} container className="upcoming-event">
        {events
          ? events
              .slice(0, maxEventCount)
              .map((event) => <EventCard event={event} key={event.slug} />)
          : LoadingSkeleton}
      </Grid>
    </Card>
  );
  const myClubsSection = (
    <Card variant="outlined" className="card">
      <SectionTitle title={t('home.myClubs')} url="/club" />
      <Grid container>
        {myClubs
          ? myClubs.map((item) => (
              <ClubAvatar
                name={item.name}
                clubUrl={item.get_absolute_url}
                logoUrl={item.logo_url}
                key={item.name}
                size={clubAvatarSize}
              />
            ))
          : [0, 1, 2].map((item) => (
              <Skeleton
                key={item}
                variant="circular"
                height={clubAvatarSize}
                width={clubAvatarSize}
                sx={{ margin: '10px' }}
              />
            ))}
      </Grid>
    </Card>
  );

  return (
    <>
      <div className="header">
        <img className="header-image" alt="" src={headerImageURL} />
        <div id="header-title">
          <Typography id="second-title">{t('home.welcomeTo')}</Typography>
          <div id="title">
            <SvgIcon
              component={NantralIcon}
              inheritViewBox
              sx={{
                height: 50,
                width: 50,
                display: { xs: 'none', md: 'flex' },
              }}
            />
            <Typography id="main-title">Nantral Platform</Typography>
          </div>
        </div>
      </div>
      <div style={{ alignContent: 'center', display: 'flex' }}>
        <div className="container">
          <PostSection
            posts={posts.filter((post) => post.pinned)}
            title={t('home.highlighted')}
            status={postsStatus}
          />
          <PostSection
            posts={posts.filter((post) => !post.pinned)}
            title={t('home.announcement')}
            status={postsStatus}
          />
          <EventSection
            events={events.filter((item: EventProps) =>
              isThisWeek(new Date(item.beginDate))
            )}
            status={eventsStatus}
            seeMoreUrl="/event"
            title={t('home.thisWeek')}
          />
          <EventSection
            events={events.filter(
              (item: EventProps) => !isThisWeek(new Date(item.beginDate))
            )}
            status={eventsStatus}
            maxItem={3}
            seeMoreUrl="/event"
            title={t('home.upcomingEvents')}
          />
          <ClubSection
            clubs={myClubs}
            status={clubsStatus}
            title={t('home.myClubs')}
            seeMoreUrl="/club"
          />
        </div>
      </div>
    </>
  );
}

function SectionTitle(props: { title: string; url: string }): JSX.Element {
  const { t } = useTranslation('translation'); // translation module
  const { title, url } = props;
  return (
    <span className="section">
      <h1>{title}</h1>
      <NavLink to={url} className="see-more">
        <Button>{t('home.seeMore')}</Button>
      </NavLink>
    </span>
  );
}

export default Home;
