function Navbar() {

    const [isLoggedIn, setIsLoggedIn] = React.useState(false);
    const [user, setUser] = React.useState({}); 
    
    React.useEffect(() => {
        fetch('/api/user')
            .then((response) => response.json())
            .then((responseJson) => {
                if ('firstName' in responseJson.user && 'lastName' in responseJson.user) {
                    setUser(responseJson.user);
                    setIsLoggedIn(true);
                } 
            });
    }, []);

    return (
        <ReactBootstrap.Navbar bg='light' expand='lg' className='mb-4'>
            <ReactBootstrap.Container fluid>
                <ReactBootstrap.Navbar.Brand href='/'>FoodieFriend</ReactBootstrap.Navbar.Brand>
                <ReactBootstrap.Navbar.Toggle aria-controls='navbar-text' />
                <ReactBootstrap.Navbar.Collapse id='navbar-text'>
                    <ReactBootstrap.Nav className='me-auto mb-2 mb-lg-0'>
                        <ReactBootstrap.Nav.Item>
                            <ReactBootstrap.Nav.Link href='/'>Home</ReactBootstrap.Nav.Link>
                        </ReactBootstrap.Nav.Item>
                        <ReactBootstrap.Nav.Item>
                            <ReactBootstrap.Nav.Link href='/restaurants'>Restaurants</ReactBootstrap.Nav.Link>
                        </ReactBootstrap.Nav.Item>
                        <ReactBootstrap.Nav.Item>
                            <ReactBootstrap.Nav.Link href='/users'>Users</ReactBootstrap.Nav.Link>
                        </ReactBootstrap.Nav.Item>
                    </ReactBootstrap.Nav>
                    <ReactBootstrap.Nav className='d-flex'>
                        {!isLoggedIn ? ( <><ReactBootstrap.Nav.Item>
                                            <ReactBootstrap.Nav.Link href='/login'>Log In</ReactBootstrap.Nav.Link>
                                        </ReactBootstrap.Nav.Item>
                                        <ReactBootstrap.Nav.Item>
                                            <ReactBootstrap.Nav.Link href='/signup'>Sign Up</ReactBootstrap.Nav.Link>
                                        </ReactBootstrap.Nav.Item></>)
                                    : ( <ReactBootstrap.NavDropdown title={`${user.firstName} ${user.lastName.charAt(0)}.`}>
                                            <ReactBootstrap.NavDropdown.Item href='/users'>My Account</ReactBootstrap.NavDropdown.Item>
                                            <ReactBootstrap.NavDropdown.Item href='/logout'>Log Out</ReactBootstrap.NavDropdown.Item>
                                        </ReactBootstrap.NavDropdown>)
                        }
                    </ReactBootstrap.Nav>
                </ReactBootstrap.Navbar.Collapse>
            </ReactBootstrap.Container>
        </ReactBootstrap.Navbar>
    );
}

ReactDOM.render(<Navbar />, document.querySelector('#root'));