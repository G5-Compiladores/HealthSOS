import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([{
    path: '/',
    element: <Layout />,
    children: [
        {
            index: true,
            element: <Home />
        },
        {
            path:'login',
            element: <LogIn />
        },
        {
            path:'search',
            element: <Search />
        },
        {
            path:'register',
            element: <Register />
        }
]
}])