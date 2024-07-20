import React, {useState} from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import { routeOptions, settingsOptions } from '../navigator'
import { useNavigate } from 'react-router-dom';
import MenuIcon from '@mui/icons-material/Menu';
import SettingsIcon from '@mui/icons-material/Settings';
import { RefreshModal } from '../components/modals';

const settings = Object.keys(settingsOptions);

function ResponsiveAppBar() {
  const [anchorElNav, setAnchorElNav] = useState(null);
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [isDataRefreshModalOpen, setIsDataRefreshModalOpen] = useState(false);
  const [isModelRefreshModalOpen, setIsModelRefreshModalOpen] = useState(false);

  const [originX, setOriginX] = useState(0);
  const [originY, setOriginY] = useState(0);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = (path) => {
    setAnchorElNav(null);
    navigate(path)
  };

  const handleUserMenu = (event, setting) => {
    setAnchorElUser(null);
    setOriginX(event.clientX);
    setOriginY(event.clientY);
    setting === "Refresh - Data" ? setIsDataRefreshModalOpen(true) : setIsModelRefreshModalOpen(true);
  }

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };
	
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h4"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 1000,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            PL PREDICTION
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {Object.entries(routeOptions).map(([route, obj]) => {
                if (route !== "home") {
                  return (
                    <MenuItem key={route} onClick={() => handleCloseNavMenu(obj.path)}>
                      <Typography textAlign="center">{route.toUpperCase()}</Typography>
                    </MenuItem>
                  );
                }
                return null;
              })}
            </Menu>
          </Box>
          <Typography
            variant="h5"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            PL PREDICTION
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {Object.entries(routeOptions).map(([route, obj]) => {
              if (route !== "home") {
                return (
                  <Button
                    key={route}
                    onClick={() => navigate(obj.path)}
                    sx={{ my: 2, color: 'white', display: 'block' }}
                  >
                    {route}
                  </Button>
                );
              }
              return null;
            })}
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <SettingsIcon alt="Settings" fontSize='large'/>
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              {settings.map((setting) => (
                <Tooltip key={setting} title={settingsOptions[setting].tooltip}>
                  <MenuItem key={setting} onClick={(event) => handleUserMenu(event, setting)}>
                    <Typography textAlign="center">{setting}</Typography>
                  </MenuItem>
                </Tooltip>
              ))}
            </Menu>
          </Box>
          <RefreshModal settingOptions={settingsOptions["Refresh - Data"].options} isOpen={isDataRefreshModalOpen} setIsOpen={setIsDataRefreshModalOpen} originX={originX} originY={originY} />
          <RefreshModal settingOptions={settingsOptions["Refresh - Model"].options} isOpen={isModelRefreshModalOpen} setIsOpen={setIsModelRefreshModalOpen} originX={originX} originY={originY} />
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default ResponsiveAppBar;