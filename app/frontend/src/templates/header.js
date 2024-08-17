import React, { useState } from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import Container from "@mui/material/Container";
import Button from "@mui/material/Button";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import { routeOptions, settingsOptions, menuOptions } from "../navigator";
import { useNavigate } from "react-router-dom";
import MenuIcon from "@mui/icons-material/Menu";
import SettingsIcon from "@mui/icons-material/Settings";
import { RefreshModal } from "../components/modals";

const settings = Object.keys(settingsOptions);

// Add dropdown menu for each of:
//     Stats - Players, Teams, Managers, Matches
//     Prediction - Upcoming Results, Match Facts
//     FPL - Player search, Solver

function ResponsiveAppBar() {
	const [anchorElNav, setAnchorElNav] = useState(null);
	const [anchorElUser, setAnchorElUser] = useState(null);
	const [isDataRefreshModalOpen, setIsDataRefreshModalOpen] = useState(false);
	const [isModelRefreshModalOpen, setIsModelRefreshModalOpen] = useState(false);
	const [currentPage, setCurrentPage] = useState(window.location.pathname);

	const [originX, setOriginX] = useState(0);
	const [originY, setOriginY] = useState(0);
  const open = Boolean(anchorElNav);
  const navigate = useNavigate();

	const handleOpenUserMenu = (event) => {
		setAnchorElUser(event.currentTarget);
	};

	const handleUserMenu = (event, setting) => {
		setAnchorElUser(null);
		setOriginX(event.clientX);
		setOriginY(event.clientY);
		setting === "Refresh - Data"
			? setIsDataRefreshModalOpen(true)
			: setIsModelRefreshModalOpen(true);
	};

	const handleCloseUserMenu = () => {
		setAnchorElUser(null);
  };
  
  const [anchorEl, setAnchorEl] = useState(null);
  const [openMenu, setOpenMenu] = useState(null);


  const handleOpenNavMenu = (event, menu) => {
    setAnchorEl(event.currentTarget);
    setOpenMenu(menu);
  };

  const handleCloseNavMenu = (path) => {
    setAnchorEl(null);
    setOpenMenu(null);
  };


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
							display: { xs: "none", md: "flex" },
							fontFamily: "monospace",
							fontWeight: 1000,
							letterSpacing: ".3rem",
							color: "inherit",
							textDecoration: "none",
						}}
					>
						PL PREDICTION
					</Typography>
					<Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
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
								vertical: "bottom",
								horizontal: "left",
							}}
							keepMounted
							transformOrigin={{
								vertical: "top",
								horizontal: "left",
							}}
							open={Boolean(anchorElNav)}
							onClose={handleCloseNavMenu}
							sx={{
								display: { xs: "block", md: "none" },
							}}
						>
							{Object.entries(routeOptions).map(([route, obj]) => {
								if (route !== "home") {
									return (
										<MenuItem
											key={route}
											onClick={() => handleCloseNavMenu(obj.path)}
										>
											<Typography textAlign="center">
												{route.toUpperCase()}
											</Typography>
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
							display: { xs: "flex", md: "none" },
							flexGrow: 1,
							fontFamily: "monospace",
							fontWeight: 700,
							letterSpacing: ".3rem",
							color: "inherit",
							textDecoration: "none",
						}}
					>
						PL PREDICTION
					</Typography>
					<Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
						{Object.entries(menuOptions).map(([menu, options]) => (
							<Box key={menu}>
								<Button
									onClick={(event) => handleOpenNavMenu(event, menu)}
									sx={{ my: 2, color: "white", display: "block" }}
								>
									{menu}
								</Button>
								<Menu
									id={`menu-${menu}`}
									anchorEl={anchorEl}
									open={openMenu === menu}
									onClose={handleCloseNavMenu}
									MenuListProps={{
										"aria-labelledby": `menu-button-${menu}`,
									}}
								>
									{Object.entries(options).map(([title, { path }]) => (
										<MenuItem
											key={title}
											onClick={() => {
												if (path) {
													navigate(path);
												}
												handleCloseNavMenu();
											}}
										>
											{title}
										</MenuItem>
									))}
								</Menu>
							</Box>
						))}
					</Box>

					<Box sx={{ flexGrow: 0 }}>
						<Tooltip title="Open settings">
							<IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
								<SettingsIcon alt="Settings" fontSize="large" />
							</IconButton>
						</Tooltip>
						<Menu
							sx={{ mt: "45px" }}
							id="menu-appbar"
							anchorEl={anchorElUser}
							anchorOrigin={{
								vertical: "top",
								horizontal: "right",
							}}
							keepMounted
							transformOrigin={{
								vertical: "top",
								horizontal: "right",
							}}
							open={Boolean(anchorElUser)}
							onClose={handleCloseUserMenu}
						>
							{settings.map((setting) => (
								<Tooltip key={setting} title={settingsOptions[setting].tooltip}>
									<MenuItem
										key={setting}
										onClick={(event) => handleUserMenu(event, setting)}
									>
										<Typography textAlign="center">{setting}</Typography>
									</MenuItem>
								</Tooltip>
							))}
						</Menu>
					</Box>
					<RefreshModal
						settingOptions={settingsOptions["Refresh - Data"].options}
						isOpen={isDataRefreshModalOpen}
						setIsOpen={setIsDataRefreshModalOpen}
						originX={originX}
						originY={originY}
					/>
					<RefreshModal
						settingOptions={settingsOptions["Refresh - Model"].options}
						isOpen={isModelRefreshModalOpen}
						setIsOpen={setIsModelRefreshModalOpen}
						originX={originX}
						originY={originY}
					/>
				</Toolbar>
			</Container>
		</AppBar>
	);
}
export default ResponsiveAppBar;
