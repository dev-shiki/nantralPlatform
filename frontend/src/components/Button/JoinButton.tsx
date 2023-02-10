import {
  PeopleAlt as PeopleIcon,
  AddCircle as PlusIcon,
  CheckCircle as CheckIcon,
  LinkOutlined as LinkIcon,
  LocalFireDepartment as ShotgunIcon,
  Cancel as Cross,
} from '@mui/icons-material';
import { Button, Theme, SxProps, CircularProgress } from '@mui/material';
import axios from 'axios';

import * as React from 'react';

import { useTranslation } from 'react-i18next';
import { formatDate, formatTime } from '../../utils/date';
import { UnsuscribeModal } from '../Modal/UnsuscribeModal';

interface JoinButtonProps {
  variant?: 'shotgun' | 'normal' | 'form';
  link?: string;
  maxPerson?: number;
  person: number;
  sx?: SxProps<Theme>;
  participating: boolean;
  eventSlug: string;
  beginInscription: string | null;
  endInscription: string | null;
}

function JoinButton({
  variant,
  link,
  maxPerson,
  person,
  sx,
  participating,
  eventSlug,
  beginInscription,
  endInscription,
}: JoinButtonProps): JSX.Element {
  const [selected, setSelected] = React.useState(participating);
  const [people, setPeople] = React.useState(person);
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  const { t } = useTranslation('translation');
  const closed: boolean =
    (variant === 'shotgun' && person >= maxPerson) ||
    (endInscription !== null &&
      Date.now() > new Date(endInscription).getTime());
  const inscriptionNotStarted: boolean =
    beginInscription !== null &&
    Date.now() < new Date(beginInscription).getTime();

  const participate = async () => {
    axios
      .post(`api/event/${eventSlug}/participate`)
      .then((res) => {
        if (res.data.success) {
          setPeople(people + 1);
          setSelected(true);
        } else {
          console.error('could not subscribe to event');
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  const quit = async () => {
    axios
      .delete(`api/event/${eventSlug}/participate`)
      .then((res) => {
        if (res.data.success) {
          setSelected(false);
          setPeople(people - 1);
        } else {
          console.error('could not unsuscribe from event');
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  const handleClose = (unsuscribe: boolean) => {
    setOpen(false);
    if (unsuscribe) {
      setLoading(true);
      quit();
    }
  };
  const onClick = () => {
    switch (variant) {
      case 'normal':
        if (closed || inscriptionNotStarted) return;
        if (selected) {
          setOpen(true);
        } else {
          setLoading(true);
          participate();
        }
        break;
      case 'shotgun':
        if ((closed && !selected) || inscriptionNotStarted) return;
        if (selected) {
          setOpen(true);
        } else {
          setLoading(true);
          participate();
        }
        break;
      case 'form':
        window.open(link, '_blank');
        break;
      default:
    }
  };

  const getFirstIcon = () => {
    if (inscriptionNotStarted) return null;
    switch (variant) {
      case 'shotgun':
        return <ShotgunIcon />;
      case 'form':
        return <LinkIcon />;
      default:
        return <PeopleIcon />;
    }
  };
  const getSecondIcon = () => {
    if (inscriptionNotStarted) return null;
    if (closed && variant !== 'form') return <Cross />;
    if (variant === 'normal') return selected ? <CheckIcon /> : <PlusIcon />;
    if (variant === 'shotgun') {
      if (closed && !selected) return <Cross />;
      if (selected) return <CheckIcon />;
      return selected ? <CheckIcon /> : <PlusIcon />;
    }
    return null;
  };
  const getText = () => {
    switch (variant) {
      case 'normal':
        return inscriptionNotStarted
          ? new Date(beginInscription).toLocaleTimeString()
          : people;
      case 'shotgun':
        return inscriptionNotStarted
          ? `${formatDate(new Date(beginInscription), 'short')} ${formatTime(
              new Date(beginInscription),
              'short'
            )}`
          : `${people}/${maxPerson}`;
      case 'form':
        return t('button.joinButton.register');
      default:
        return people;
    }
  };
  let title: string;
  if (variant === 'form') title = t('button.joinButton.registerLink');
  else if (closed && variant === 'shotgun')
    title = t('button.joinButton.shotgunClosed');
  else if (!selected) title = t('button.joinButton.register');
  else title = t('button.joinButton.unsuscribe');

  let color:
    | 'inherit'
    | 'primary'
    | 'secondary'
    | 'success'
    | 'error'
    | 'info'
    | 'warning';
  if (selected) {
    color = 'success';
  } else if (closed) {
    color = 'warning';
  } else {
    color = 'info';
  }
  return (
    <>
      <Button
        disabled={loading || inscriptionNotStarted || closed}
        onClick={() => onClick()}
        variant="contained"
        startIcon={getFirstIcon()}
        color={color}
        endIcon={getSecondIcon()}
        sx={sx}
        title={title}
      >
        {getText()}
        {loading && (
          <CircularProgress size={25} style={{ position: 'absolute' }} />
        )}
      </Button>
      <UnsuscribeModal open={open} onClose={handleClose} />
    </>
  );
}

JoinButton.defaultProps = {
  variant: 'normal',
  link: '',
  maxPerson: 0,
  sx: {},
};

export default JoinButton;
