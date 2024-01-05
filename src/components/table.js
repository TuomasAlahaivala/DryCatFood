import { useState } from "react";
import TableBody from "./tableBody";
import TableHead from "./tableHead";

const Table = ({data}) => {
console.log(data);
 const [tableData, setTableData] = useState(data);
 const columns = [
  { label: "Tuote", accessor: "title", sortable: true },
  { label: "Kilohinta", accessor: "kilo_price", sortable: true },
  { label: "Proteiini", accessor: "raakaproteiini", sortable: true },
  { label: "Rasva", accessor: "raakarasva", sortable: true },
  { label: "Kuitu", accessor: "raakakuitu", sortable: true },
  { label: "Tuhka", accessor: "raakatuhka", sortable: true },
  { label: "Kalsium", accessor: "kalsium", sortable: true },
  { label: "Fosfori", accessor: "fosfori", sortable: true },
 ];

 const handleSorting = (sortField, sortOrder) => {
  if (sortField) {
    const sorted = [...tableData].sort((a, b) => {
     if (a[sortField] === null || a[sortField] === "——") return 1;
     if (b[sortField] === null) return -1;
     if (a[sortField] === undefined) return -1;
     if (a[sortField] === null && b[sortField] === null) return 0;
     if (a[sortField] === null && b[sortField] === null) return 0;
     if (a[sortField] === undefined && b[sortField] === null) return 0;
     if (b[sortField] === undefined) return 1;
     console.log(a[sortField])
     console.log(b[sortField])
     return (
      a[sortField].toString().localeCompare(b[sortField].toString(), "en", {
       numeric: true,
      }) * (sortOrder === "asc" ? 1 : -1)
     );
    });
    setTableData(sorted);
   }
 };
 return (
  <>
   <table className="table">
    <TableHead columns={columns} handleSorting={handleSorting} />
    <TableBody columns={columns} tableData={tableData} />
   </table>
  </>
 );
};

export default Table;