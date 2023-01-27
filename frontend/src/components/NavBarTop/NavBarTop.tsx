import * as React from 'react';
import i18next from 'i18next';
import InputLabel from '@mui/material/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import { useTranslation } from 'react-i18next';
import {
  IconButton,
  AppBar,
  Typography,
  Box,
  Badge,
  Toolbar,
  Menu,
  MenuItem,
  ListItemText,
} from '@mui/material';
import SvgIcon, { SvgIconProps } from '@mui/material/SvgIcon';
import Collapse from '@mui/material/Collapse';
import {
  Notifications as NotificationsIcon,
  AccountCircle,
  MoreVert as MoreIcon,
} from '@mui/icons-material';
import Divider from '@mui/material/Divider';
import GavelIcon from '@mui/icons-material/Gavel';
import PersonIcon from '@mui/icons-material/Person';
import PublicRoundedIcon from '@mui/icons-material/PublicRounded';
import HelpRoundedIcon from '@mui/icons-material/HelpRounded';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ErrorRoundedIcon from '@mui/icons-material/ErrorRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import { createSvgIcon } from '@mui/material/utils';
import { ThemeProvider } from '@mui/material/styles';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { SearchBar } from './SearchBar/SearchBar';
import './NavBarTop.scss';
import { ReactComponent as MenuIcon } from '../../assets/scalable/menu.svg';
import { ReactComponent as NotifIcon } from '../../assets/scalable/notification.svg';
import { ReactComponent as PeopleIcon } from '../../assets/scalable/people.svg';
import { ReactComponent as NantralIcon } from '../../assets/logo/scalable/logo.svg';

/**
 * The top bar for navigation
 *
 * @param props Component Properties
 * @param {boolean} props.menuOpen - A boolean to indicate if the lateral menu
 * is open or not.
 * @params props.setMenuOpen - A function to change the state of the menu.
 * @returns The top bar component
 */
function NavBarTop(props: {
  menuOpen: boolean;
  setMenuOpen: React.Dispatch<React.SetStateAction<boolean>>;
  themeApp: boolean;
  setThemeApp: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const { menuOpen, setMenuOpen, themeApp, setThemeApp } = props;

  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [anchorElLangue, setAnchorElLangue] =
    React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const openL = Boolean(anchorElLangue);
  const spanRef = React.useRef();
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClickL = () => {
    setAnchorElLangue(spanRef.current);
    setAnchorEl(null);
  };
  const handleCloseL = () => {
    setAnchorElLangue(null);
    setAnchorEl(spanRef.current);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const changeLanguage = (lng) => {
    i18next.changeLanguage(lng);
  };

  const { t } = useTranslation('translation');

  const [langue, setLangue] = React.useState('');

  const handleChangeLangue = (event: React.MouseEvent<HTMLButtonElement>) => {
    changeLanguage(event.target.value);
  };

  return (
    <AppBar position="fixed" color="secondary">
      <Toolbar>
        <IconButton
          color="inherit"
          onClick={() => setMenuOpen(!menuOpen)}
          size="large"
          edge="start"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <SvgIcon component={MenuIcon} inheritViewBox />
        </IconButton>
        <SvgIcon component={NantralIcon} inheritViewBox />
        <Box sx={{ flexGrow: 0.02 }} />
        <Typography variant="h6" component="div" color="TextPrimary">
          Nantral Platform
        </Typography>
        <Box sx={{ flexGrow: 0.9 }} />
        <SearchBar />
        <Box sx={{ flexGrow: 1.0 }} />
        <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
          <IconButton
            size="large"
            aria-label="show 17 new notifications"
            color="inherit"
          >
            <Badge badgeContent={1} color="error">
              <SvgIcon component={NotifIcon} inheritViewBox />
            </Badge>
          </IconButton>
          <IconButton
            size="large"
            edge="end"
            aria-label="account of current user"
            aria-haspopup="true"
            color="inherit"
            onClick={handleClick}
            component="span"
            ref={spanRef}
          >
            <SvgIcon component={PeopleIcon} inheritViewBox />
          </IconButton>
          <Menu
            id="basic-menu"
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
            MenuListProps={{ 'aria-labelledby': 'basic-button' }}
            TransitionComponent={Collapse}
          >
            <MenuItem onClick={handleClose}>
              <SvgIcon component={PersonIcon} />
              <ListItemText className="menuItem">
                {t('user_menu.profile')}
              </ListItemText>
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <SvgIcon component={LogoutRoundedIcon} />
              <ListItemText className="menuItem">
                {t('user_menu.logout')}
              </ListItemText>
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <SvgIcon component={ErrorRoundedIcon} />
              <ListItemText className="menuItem">
                {t('user_menu.bug')}
              </ListItemText>
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <SvgIcon component={HelpRoundedIcon} />
              <ListItemText className="menuItem">
                {t('user_menu.doc')}
              </ListItemText>
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <SvgIcon component={GavelIcon} />
              <ListItemText className="menuItem">
                {t('user_menu.legal')}
              </ListItemText>
            </MenuItem>
            <MenuItem onClick={handleClickL}>
              <SvgIcon component={PublicRoundedIcon} />
              <ListItemText className="menuItem">
                {t('user_menu.langage')}
              </ListItemText>
            </MenuItem>
            <MenuItem onClick={() => setThemeApp(!themeApp)}>
              <SvgIcon
                component={themeApp ? Brightness7Icon : Brightness4Icon}
              />
              <ListItemText className="menuItem">
                {!themeApp ? 'Dark' : 'Light'} Mode
              </ListItemText>
            </MenuItem>
          </Menu>
          <Menu
            id="basic-menu"
            anchorEl={anchorElLangue}
            open={openL}
            onClose={handleCloseL}
            MenuListProps={{ 'aria-labelledby': 'basic-button' }}
            TransitionComponent={Collapse}
          >
            <MenuItem disableRipple="true">
              <IconButton
                aria-label="account of current user"
                aria-haspopup="true"
                color="inherit"
                onClick={handleCloseL}
              >
                <SvgIcon component={ArrowBackIcon} inheritViewBox />
              </IconButton>
              <Typography className="menuTitle" variant="h6">
                Choix du langage
              </Typography>
            </MenuItem>
            <MenuItem
              value="fr-FR"
              onClick={() => i18next.changeLanguage('fr-FR')}
            >
              Français
            </MenuItem>
            <MenuItem
              value="en-GB"
              onClick={() => i18next.changeLanguage('en-GB')}
            >
              English
            </MenuItem>
          </Menu>
        </Box>
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            size="large"
            aria-label="show more"
            aria-haspopup="true"
            color="inherit"
          >
            <MoreIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default NavBarTop;
