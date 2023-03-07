import React from 'react'
import './ProfileScreen.css'
import { Link, NavLink } from "react-router-dom";
import Footer from '../../components/Footer/Footer';
import useFetchGetAuth from '../../hooks/useFetchGetAuth'

const ProfileScreen = () => {
    const { data } = useFetchGetAuth('http://127.0.0.1:8000/api/orders')
    return (
        <>
            <div className='ProfileContainer'>
                <div className='ProfileContainer1'>
                    <h1 className='ProfileContainer1H1'>Your Orders</h1>
                    <div className='ProfileContainer1Header'>
                        <NavLink className={({ isActive }) => (isActive ? 'ProfileContainer1HeaderBtn' : 'ProfileContainer1HeaderBtnDis')} to={'/profile'}>Orders</NavLink>
                        <NavLink className={({ isActive }) => (isActive ? 'ProfileContainer1HeaderBtn' : 'ProfileContainer1HeaderBtnDis')} to={'/settings'}>Settings</NavLink>
                    </div>
                    <div className='ProfileContainer1Main'>
                        <div className='ProfileContainer1MainBlock1'>
                            <h1 className='ProfileContainer1MainBlockH1Top'>Order ID</h1>
                            <p className='ProfileContainer1MainBlockPTop'>Data Ordered</p>
                            <p className='ProfileContainer1MainBlockPriceTop'>Price</p>
                            <button className='ProfileContainer1MainBlockBtnTop'>Action</button>
                        </div>
                        {data && data['orders'].map((item) => (
                            <Link to={'/profile'} className='ProfileContainer1MainBlock' key={item.id}>
                                <div className='ProfileContainer1MainBlockDiv'>
                                    <h1 className='ProfileContainer1MainBlockH1'>Order #{item.id}</h1>
                                    <p className='ProfileContainer1MainBlockP'>{item.dataOrdered.substring(0, 10)}</p>
                                </div>
                                <div className='ProfileContainer1MainBlockDiv1'>
                                    <p className='ProfileContainer1MainBlockPrice'>${item['order_total']}</p>
                                    <button className='ProfileContainer1MainBlockBtn'>See Order</button>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </div>
            <Footer/>
        </>
    )
}

export default ProfileScreen