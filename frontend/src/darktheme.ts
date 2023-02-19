import { createTheme } from '@mui/material/styles';

const darktheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#dc3545',
    },
    secondary: {
      main: '#efefef',
    },
    button: {
      main: '0d6efd',
    },
    warning: {
      main: '#dc3545',
    },
    info: {
      main: '#0d6efd',
    },
    background: {
      default: '#212121',
      paper: '#252525',
    },
    text: {
      primary: '#fff',
    },
    success: {
      main: '#2e7d32',
    },
  },
  overrides: {
    MuiAppBar: {
      colorInherit: {
        backgroundColor: '#689f38',
        color: '#fff',
      },
    },
  },
  props: {
    MuiAppBar: {
      color: 'secondary',
    },
  },
});

export default darktheme;
